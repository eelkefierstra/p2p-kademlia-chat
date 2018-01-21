#!/usr/bin/env python3

"""
The tracker server
"""

import json
import uuid
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
        chatresponse = json.dumps(chatresponse_json)

        return chatresponse

    def send_message(self, msg_json):
        chatuuid = msg_json["chatuuid"]
        msg_hash = msg_json["hash"]

        self.db.store_message(chatuuid, msg_hash)

        sendmsg_json = {
            "action" : "sendmessage",
            "chatuuid" : chatuuid,
            "msg_hash" : msg_hash
        }

        sendmsg_response = json.dumps(sendmsg_json)
        return sendmsg_response

    """
    Get the messages from fromtime till tilltime
    """
    def get_messages(self, chatuuid):
        #TODO Actually get the messages
        #TODO 0 -> from time
        chatmessages_json = {
            "action" : "getmessages",
            "fromtime" : 0,
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

        chatmessages = json.dumps(chatmessages_json)
        return chatmessages
    
    """
    Not sure when we received the full data, so maybe use a delimiter or
    send the length in the request.
    """
    def dataReceived(self, data):
        json_obj = json.loads(data)
        action = json_obj["action"]
        if action  == "createchat":
            response = self.create_chat()
        elif action == "sendmessage":
            response = self.send_message(json_obj)
        elif action == "getmessages":
            response = self.get_messages(json_obj)

        self.transport.write(response.encode('utf-8'))


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
        # TODO load these values from a config file?

        from twisted.internet import reactor

        port = reactor.listenTCP(self.port, factory, interface=self.interface)
        reactor.run()


