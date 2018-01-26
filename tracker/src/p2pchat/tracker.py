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
        self.db.create_chat(chatuuid)
        chatresponse_json = {
            "action" : "createchat",
            "chatuuid" : str(chatuuid)
        }
        return chatresponse_json

    def send_message(self, msg_json):
        # TODO keyerror
        chatuuid = msg_json["chatuuid"]
        msg_hash = msg_json["msg_hash"]

        self.db.store_message(chatuuid, msg_hash)

        sendmsg_json = {
            "action" : "sendmessage",
            "chatuuid" : chatuuid,
            "msg_hash" : msg_hash
        }

        return sendmsg_json



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
                "action" : "getmessages",
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
                ]
            }
            self.write_json(chatmessages_json)
            #TODO actually do something useful with the messages
            print("got_messages: {}".format(messages))

        d = self.db.get_messages(uuid, fromtime_date)
        print(type(d))
        d.addCallback(write_get_messages) 


    def write_json(self, json_obj):
        response = json.dumps(json_obj)
        self.transport.write(response.encode('utf-8'))
    
    """
    Not sure when we received the full data, so maybe use a delimiter or
    send the length in the request.
    """
    def dataReceived(self, data):
        json_obj = json.loads(data)
        #TODO keyerror
        action = json_obj["action"]
        if action  == "createchat":
            jsonresponse = self.create_chat()
            self.write_json(jsonresponse)
        elif action == "sendmessage":
            jsonresponse = self.send_message(json_obj)
            self.write_json(jsonresponse)
        elif action == "getmessages":
            # TODO async
            jsonresponse = self.get_messages(json_obj)



class TrackerFactory(ServerFactory):
    

    """
    db: instance of P2PChatDB
    """
    def __init__(self, db):
        self.db = db

    def buildProtocol(self):
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


