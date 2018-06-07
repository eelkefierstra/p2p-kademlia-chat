#!/usr/bin/env python3

"""
The tracker server
"""

import sys
import json
import uuid
import datetime
import time
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import NetstringReceiver
from p2pchat.database import P2PChatDB


class TrackerProtocol(NetstringReceiver):

    def __init__(self, factory, db):
        self.factory = factory
        self.db = db
        self.joinedchats = set()

    def create_chat(self):
        # TODO create unit test to see if the chat is created
        chatuuid = str(uuid.uuid4())

        def write_created_chat():
            chatresponse_json = {
                "action": "createdchat",
                "chatuuid": chatuuid
            }
            print("Chat created, notifying client")
            self.write_json(chatresponse_json)

        print("Creating new chat with uuid: {}".format(chatuuid))
        d = self.db.create_chat(chatuuid)
        d.addCallback(lambda x: write_created_chat())
        # Add this client to the notiviables of the chat
        d.addCallback(lambda x: self._get_notifications([chatuuid]))

    def send_message(self, msg_json):
        print("New message received")
        # TODO keyerror
        chatuuid = msg_json["chatuuid"]
        msg_hash = msg_json["msg_hash"]
        timesent = datetime.datetime.now()
        timesent_ts = timesent.timestamp()

        def write_message_sent(result):
            sendmsg_json = {
                "action": "sentmessage",
                "chatuuid": chatuuid,
                "msg_hash": msg_hash,
                "time_sent": timesent_ts
            }
            print("New message stored in DB, notifying client")
            self.write_json(sendmsg_json)

        d = self.db.store_message(chatuuid, msg_hash, timesent)
        d.addCallback(write_message_sent)
        # Update the other clients about a message being sent
        self.factory.push_message(self, chatuuid, msg_hash, timesent_ts)

    def get_notifications(self, notification_json):
        chatuuids = notification_json["chats"]
        self._get_notifications(chatuuids)

    def _get_notifications(self, chatuuids):
        for chatuuid in chatuuids:
            if chatuuid not in self.factory.notiviables:
                self.factory.notiviables[chatuuid] = set()

            self.joinedchats.add(chatuuid)
            self.factory.notiviables[chatuuid].add(self)

    def push_message(self, chatuuid, msg_hash, time_sent):
        chatmsg_json = {
                "action": "gotmessage",
                "chatuuid": chatuuid,
                "msg_hash": msg_hash,
                "time_sent": time_sent
            }
        self.write_json(chatmsg_json)
        print("Push notificatio new message send")

    """
    Get the messages from fromtime till tilltime
    """
    def get_messages(self, msg_request_json):
        fromtime = int(msg_request_json["fromtime"])
        fromtime_date = datetime.datetime.fromtimestamp(fromtime)
        tilltime = int(time.time())
        uuid = msg_request_json["chatuuid"]

        """
        Callback for writing messages to the tracker client
        """
        def write_get_messages(messages_results):
            # TODO Actually get the messages
            messages = []
            for messages_result in messages_results:
                messages.extend(
                    {
                        "hash": message["hash"],
                        "time": message["time"].timestamp()
                    } for message in messages_result['messages']
                )

            chatmessages_json = {
                "action": "gotmessages",
                "fromtime": fromtime,
                "tilltime": tilltime,
                "messages": messages,
                "chatuuid": uuid
            }
            self.write_json(chatmessages_json)
            # TODO actually do something useful with the messages

        d = self.db.get_messages(uuid, fromtime_date)
        d.addCallback(write_get_messages)

    def write_json(self, json_obj):
        response = json.dumps(json_obj)
        # self.transport.write(response.encode('utf-8'))
        self.sendString(response.encode('utf-8'))

    def connectionMade(self):
        # self.factory.protocols.append(self)
        ip_addr = self.transport.getPeer().host
        print("[*] New client connected: {}".format(ip_addr))

    # def connectionLost(self, reason):
    #    #self.factory.protocols.remove(self)

    def stringReceived(self, string):
        try:
            json_obj = json.loads(string.decode('utf-8'))
        except UnicodeError:
            # discard input which is not
            print("Can't decode to utf-8, discarding input.", file=sys.stderr)
            return
        except json.JSONDecodeError:
            print("Can't decode JSON, discarding input.", file=sys.stderr)
            return
        # TODO keyerror
        action = json_obj["action"]
        if action == "createchat":
            self.create_chat()
        elif action == "get_notified":
            self.get_notifications(json_obj)
        elif action == "sendmessage":
            self.send_message(json_obj)
        elif action == "getmessages":
            self.get_messages(json_obj)


class TrackerFactory(ServerFactory):

    """
    db: instance of P2PChatDB
    """
    def __init__(self, db):
        self.db = db
        self.notiviables = {}

    def buildProtocol(self, addr):
        return TrackerProtocol(self, self.db)

    def push_message(self, protocol, chatuuid, msg_hash, time_sent):
        # only send to protocols who are registered to chatuuid
        if chatuuid not in self.notiviables:
            return

        for prot in self.notiviables[chatuuid]:
            if prot != protocol:
                prot.push_message(chatuuid, msg_hash, time_sent)


class Tracker:

    def __init__(self, iface, port, db):
        self.interface = iface
        self.port = port
        self.db = db

    def start(self, reactor):
        factory = TrackerFactory(self.db)

        # TODO load these values from a config file?
        reactor.listenTCP(self.port, factory, interface=self.interface)
