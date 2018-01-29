#!/usr/bin/env python3

"""
The tracker server
"""

import json
import uuid
import datetime
import time
import hashlib
from twisted.internet import defer
from twisted.internet.protocol import ServerFactory, Protocol
from p2pchat.database import P2PChatDB

class TrackerProtocol(Protocol):

    def __init__(self, db):
        self.db = db

    def create_chat(self):
        #TODO create unit test to see if the chat is created
        chatuuid = uuid.uuid4()

        def write_created_chat(result):
            chatresponse_json = {
                "action" : "createdchat",
                "chatuuid" : str(chatuuid)
            }
            self.write_json(chatresponse_json)

        d = self.db.create_chat(chatuuid)
        d.addCallback(write_created_chat)


    def send_message(self, msg_json):
        # TODO keyerror
        chatuuid = msg_json["chatuuid"]
        msg_hash = msg_json["msg_hash"]

        def write_message_sent(result):
            sendmsg_json = {
                "action" : "sentmessage",
                "chatuuid" : chatuuid,
                "msg_hash" : msg_hash
            }
            self.write_json(sendmsg_json)

        d = self.db.store_message(chatuuid, msg_hash)
        d.addCallback(write_message_sent)

    """
    Get the messages from fromtime till tilltime
    """
    def get_messages(self, msg_request_json):
        fromtime = msg_request_json["fromtime"]
        fromtime_date = datetime.datetime.fromtimestamp(fromtime)
        uuid = msg_request_json["chatuuid"]

        """
        Callback for writing messages to the tracker client
        """
        def write_get_messages(messages):
            #TODO Actually get the messages
            chatmessages_json = {
                "action" : "gotmessages",
                "fromtime" : fromtime,
                "tilltime" : time.time(),
                "messages" : 
                [
                    {
                        "time" : 4,
                        "hash" : hashlib.sha256(b"foo").hexdigest()
                    },
                    {
                        "time" : 4,
                        "hash" : hashlib.sha256(b"bar").hexdigest()
                    }
                ],
                "chatuuid" : uuid
            }
            self.write_json(chatmessages_json)
            #TODO actually do something useful with the messages

        d = self.db.get_messages(uuid, fromtime_date)
        d.addCallback(write_get_messages) 


    def write_json(self, json_obj):
        response = json.dumps(json_obj)
        self.transport.write(response.encode('utf-8'))
    
    def connectionMade(self):
        print("connected....")

    """
    Not sure when we received the full data, so maybe use a delimiter or
    send the length in the request.
    """
    def dataReceived(self, data):
        json_obj = json.loads(data)
        #TODO keyerror
        action = json_obj["action"]
        if action  == "createchat":
            self.create_chat()
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

    def buildProtocol(self, addr):
        return TrackerProtocol(self.db)

class Tracker: 

    def __init__(self, iface, port, db):
        self.interface = iface
        self.port = port
        self.db = db

    def start(self):
        factory = TrackerFactory(self.db)

        from twisted.internet import reactor
        # TODO load these values from a config file?
        port = reactor.listenTCP(self.port, factory, interface=self.interface)
        reactor.run()


