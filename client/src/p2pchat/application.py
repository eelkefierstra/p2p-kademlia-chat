#!/usr/bin/env python3
'''
@author: Eelke
Interface for UI to communicate to core
'''
from twisted.internet.defer import inlineCallbacks
from p2pchat.trackerclient import ITrackerNotifier
from p2pchat.ui_interface import UIInterface
from tkinter import *
from twisted.internet import tksupport, reactor
import queue


class Application(ITrackerNotifier):

    def __init__(self, p2pObject, dbConnection):
        self.p2p = p2pObject
        #self.tracker = trackerclient
        self.db_conn = dbConnection
        
        root = Tk()
        # This fixes the reactor error on closing root window with the 'X' button
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
        
    def tracker_connected(self, proto):
        self.tracker_protocol = proto

    def tracker_unavailable(self, err):
        # TODO popup instead of print
        if type(err) == twisted.internet.error.ConnectionRefusedError:
            print("The tracker is currently unavailable, try again later.");
        reactor.stop()

    
    def create_chat(self, chatname):
        print("Creating chat")
        self.chatinfoqueue.put(chatname)
        # Safe group info in the p2p network
        self.tracker_protocol.create_chat()
        #def chat_created(self, chatuuid):
        #    #TODO

    def join_chat(self, chatuuid):
        def got_chat_info(chatinfo):
            print("Chat name: {}".format(chatinfo["name"]))
            # TODO set chat with chatuuid to chatname chatinfo["name"]
            # First join, download all messages
            self.tracker_protocol.get_messages(chatuuid, 0)
            chatuuids = [chatuuid]
            # Request message push updates
            self.tracker_protocol.receive_notifications(chatuuids)

        d = self.p2p.get_chat_info(chatuuid)
        d.addCallback(got_chat_info)

        def no_chat_info(err):
            print("failed to retrieve chat info: {}".format(err))
        d.addErrback(no_chat_info)


    
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
        self.db_conn.insert_new_chat(chatname, chatuuid)
        self.gui.refresh_chat_list()

    def on_message_sent(self, chatuuid, msg_hash):
        """
        Called when a message is sent to the tracker
        """
        print("Message sent to tracker: {};{}".format(chatuuid, msg_hash))

    def on_messages_received(self, chatuuid, fromtime, tilltime, messages):
        """
        Called when messages are received from the tracker
        """
        print("Messages received from tracker: {} {} {} {}".format(chatuuid, fromtime, tilltime, messages))
        
        for message in messages:
            message_hash = message['hash']
            message_time = message['time']
            message_content = self.p2p.get(message_hash)
            self.db_conn.insert_message(message_hash, message_content, message_time, chatuuid)
            
        self.gui.refresh_chat_messages()

    def on_message_received(self, chatuuid, msg_hash, time_sent):
        """
        Called when a message is pushed by the tracker
        """
        print("Received message from tracker: {} {} {}".format(chatuuid, msg_hash, time_sent))
        message_content = self.p2p.get(msg_hash)
        self.db_conn.insert_message(msg_hash, message_content, time_sent, chatuuid)
        
        self.gui.refresh_chat_messages()
