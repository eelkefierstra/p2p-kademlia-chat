#!/usr/bin/env python3

"""
The tracker server
"""

import json
import uuid
from twisted.internet.protocol import ServerFactory, Protocol
from p2pchat.database import P2PChatDB

class TrackerProtocol(Protocol):

    def create_chat(self):
        #TODO create the chat in the factory?
        print("Creating chat...")
        chatuuid = uuid.uuid4()
        self.db.create_chat(chatuuid)
        chatresponse_json = {
            "action" : "createchat",
            "chatuuid" : str(chatuuid)
        }
        chatresponse = json.dumps(chatresponse_json)

        return chatresponse

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
            print("create a chat")
            response = create_chat()
        elif action == "getmessages":
            print("Send some messages")
            response = get_messages(json_obj)
            #print("give some messages")
        self.transport.write(response)


class TrackerFactory(ServerFactory):
    
    protocol = TrackerProtocol

    """
    db: instance of P2PChatDB
    """
    def __init__(self, db):
        self.db = db

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


