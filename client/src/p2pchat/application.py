#!/usr/bin/env python3
'''
@author: Eelke
Interface for UI to communicate to core
'''
from twisted.internet.defer import inlineCallbacks
from p2pchat.trackerclient import ITrackerNotifier
from p2pchat.ui_interface import UIInterface
from tkinter import *
from twisted.internet import tksupport
import queue
import sys


class Application(ITrackerNotifier):

    def __init__(self, p2pObject, dbConnection):
        self.p2p = p2pObject
        #self.tracker = trackerclient
        self.db_conn = dbConnection

        root = Tk()
        # This fixes the reactor error on closing root window with the 'X' button
        from twisted.internet import reactor
        root.protocol("WM_DELETE_WINDOW", reactor.stop)
        self.gui = UIInterface(root, self)
        self.gui.master.title('Independed chat')
        tksupport.install(root)

        self.chatinfoqueue = queue.Queue()

    def set_trackerclient(self, trackerclient):
        self.tracker = trackerclient

    def start(self):
        d = self.tracker.connect()
        d.addCallback(self.tracker_connected)
        d.addErrback(self.tracker_unavailable)
        d.addCallback(lambda x: self.get_missed_messages())
        d.addCallback(lambda x: self.request_chatnotifications())

    def tracker_connected(self, proto):
        self.tracker_protocol = proto

    def get_missed_messages(self):
        d = self.get_chat_list()
        def got_chat_list(chat_list):
            if not chat_list:
                # nothing to do, no chats == no messages
                raise ValueError("No chats found, so no messages to download.")
            for chatname, chatuuid in chat_list:
                # Get messages for each chat
                def got_latest_msg_ts(last_msg_ts):
                    self.tracker_protocol.get_messages(chatuuid, last_msg_ts)

                d2 = self.db_conn.get_latest_msg_ts(chatuuid)
                d2.addCallback(got_latest_msg_ts)

        def got_no_chats(failure):
            failure.trap(ValueError)
            print(failure.getErrorMessage(), file=sys.stderr)
        d.addCallback(got_chat_list)
        d.addErrback(got_no_chats)



    def request_chatnotifications(self):
        # Send notification request for all existing chats
        def got_chat_list(joined_chats):
            if not joined_chats:
                return

            if len(joined_chats) > 0:
                chatuuid_list = [chatuuid for chatname, chatuuid in joined_chats]
                self.tracker_protocol.receive_notifications(chatuuid_list)
        deferred_chat_list = self.get_chat_list()
        deferred_chat_list.addCallback(got_chat_list)


    def tracker_unavailable(self, err):
        # TODO popup instead of print
        if type(err) == twisted.internet.error.ConnectionRefusedError:
            print("The tracker is currently unavailable, try again later.");

        from twisted.internet import reactor
        reactor.stop()


    def create_chat(self, chatname):
        print("Creating chat")
        self.chatinfoqueue.put(chatname)
        # Safe group info in the p2p network
        self.tracker_protocol.create_chat()
        #def chat_created(self, chatuuid):
        #    #TODO

    def join_chat(self, chatuuid):
        # TODO check if this chat is already in the db, if so, just do nothing
        chatinfo = self.p2p.get_chat_info(chatuuid)
        if not chatinfo:
            self.gui.popup_warning("Join failed", "Failed to retrieve chat info")
            return

        print("Chat name: {}".format(chatinfo["name"]))
        # First join, download all messages
        # TODO when closing the application and reopening, old chats should
        # still bee in the chat_uuid_list.
        # Probably we should not use the gui for this information
        self.tracker_protocol.get_messages(chatuuid, 0)
        d = self.db_conn.insert_new_chat(chatinfo["name"], chatuuid)
        def finish_join_chat(result):
            # Request message push updates
            # self.tracker_protocol.receive_notifications(self.gui.chat_uuid_list)
            self.tracker_protocol.receive_notifications([chatuuid])
        d.addCallback(finish_join_chat)



    def remove_chat(self, chatuuid):
        messagehash = self.p2p.send('User left chat.')
        self.db_conn.deleteChat(chatName, chatuuid)
        # TODO: Only send left chat message?
        return

    def get_chat_messages(self, chatuuid):
        return self.db_conn.get_chat_messages(chatuuid)

    def send_chat_message(self,  chat_uuid, message):
        print("Start sending message: '{}'".format(message))
        try:
            message_str = str(message)
            messagehash = self.p2p.send(message_str)
            print("Message stored in P2P-network")
            self.tracker_protocol.send_message(chat_uuid, messagehash)
        except Exception:
            # Could not make a string from message input
            # If you get here, you done something very wrong!!!
            pass
        return

    def get_chat_list(self):
        return self.db_conn.get_chat_list()

    def on_chat_created(self, chatuuid):
        """
        Called when a chat is created
        """
        # TODO set p2p info
        print("Created chat on tracker with chatuuid: {}".format(chatuuid))
        chatname = self.chatinfoqueue.get()
        # TODO sanity checks on chatname
        self.p2p.set_chat_info(chatuuid, chatname)
        d = self.db_conn.insert_new_chat(chatname, chatuuid)
        # use lambda, because refresh_chat_list takes no args
        d.addCallback(lambda x: self.gui.refresh_chat_list())
        d.addErrback(print)

    def on_message_sent(self, chatuuid, msg_hash, time_sent):
        """
        Called when a message is sent to the tracker
        """
        print("Received message from tracker: {} {} {}".format(chatuuid, msg_hash, time_sent))
        message_content = self.p2p.get(msg_hash)
        d = self.db_conn.insert_message(msg_hash, message_content, time_sent, chatuuid)
        d.addErrback(print)
        d.addCallback(self.gui.refresh_chat_messages)

    def on_messages_received(self, chatuuid, fromtime, tilltime, messages):
        """
        Called when messages are received from the tracker
        """
        print("Messages received from tracker: {} {} {} {}".format(chatuuid, fromtime, tilltime, messages))

        def got_latest_msg_ts(msg_ts):
            if msg_ts != fromtime:
                # Discard this message update, as the fromtime is later than
                # the latest update time.
                raise ValueError(
                            "fromtime != previous tilltime: fromtime = {}"
                            " and previous tilltime = {}.".format(fromtime, msg_ts)
                        )
            # Set the latest update time to tilltime
            # TODO add as deferred callback?
            self.db_conn.set_latest_msg_ts(chatuuid, tilltime)

        def latest_ts_mismatch(failure):
            failure.trap(ValueError)
            print(failure.getErrorMessage(),file=sys.stderr)

        d = self.db_conn.get_latest_msg_ts(chatuuid)
        d.addCallback(got_latest_msg_ts)
        d.addErrback(latest_ts_mismatch)

        def p2p_download_messages():
            # TODO CHANGE d to something else!!!
            d2 = None
            for message in messages:
                message_hash = message['hash']
                message_time = message['time']
                message_content = self.p2p.get(message_hash)
                d2 = self.db_conn.insert_message(message_hash, message_content, message_time, chatuuid)
                d2.addErrback(print)

            # Refresh GUI only when new messages were downloaded
            if (d2 == None):
                return
            else:
                d2.addCallback(self.gui.refresh_chat_messages)

        # TODO check if this callback is still fired when latest_ts_mismatch is
        # called
        d.addCallback(lambda x: p2p_download_messages())
        d.addErrback(print)

    def on_message_received(self, chatuuid, msg_hash, time_sent):
        """
        Called when a message is pushed by the tracker
        """
        print("Received message from tracker: {} {} {}".format(chatuuid, msg_hash, time_sent))
        message_content = self.p2p.get(msg_hash)
        d = self.db_conn.insert_message(msg_hash, message_content, time_sent, chatuuid)
        d.addErrback(print)
        d.addCallback(self.gui.refresh_chat_messages)
