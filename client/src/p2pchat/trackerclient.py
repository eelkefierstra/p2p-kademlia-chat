#!/usr/bin/env python3

"""
The p2p tracker client
"""

from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
import json


class TrackerClientProtocol(Protocol):

    def create_chat(self):
        createchat_json = {
                "action"  : "createchat"
        }
        createchat_str = json.dumps(createchat_json)
        self.transport.write(createchat_str.encode('utf-8'))

    def send_message(self, chatuuid, msg_hash):
        sendmsg_json = {
            "action" : "sendmessage",
            "chatuuid" : chatuuid,
            "msg_hash" : msg_hash
        }
        sendmsg_str = json.dumps(sendmsg_json)
        self.transport.write(sendmsg_str.encode('utf-8'))

    """
    @param fromtime Receive messages after fromtime (unix timestamp utc)
    """
    def get_messages(self, fromtime):
        pass

    def parse_new_chat(self, chatJSON):
        chatuuid = chatJSON["chatuuid"]
        # TODO do something with this new chatuuid
        print("[*] Created new chat with uuid: {}".format(chatuuid))

    def parse_messages(self, messagesJSON):
        # TODO if fromtime >= lastmsg_time, we missed some messages.
        # get the messages from lastmsg_time till fromtime also
        fromtime = messagesJSON["fromtime"]
        # TODO update the newest chat message time
        tilltime = messagesJSON["tilltime "]
        print("[*] Got a new message, fromtime: {}, tilltime: {}".format(fromtime,tilltime))

    def dataReceived(self, data):
        dataJSON = json.loads(data)
        action = dataJSON["action"]
        if action == "createchat":
            # Created new chat
            self.parse_new_chat(dataJSON)
        elif action == "getmessages":
            # New message locations arrived
            self.parse_messages(dataJSON)


class TrackerClientFactory(ClientFactory):

    def __init__(self):
        self.lastmsg_time = 0

    def buildProtocol(self, addr):
        return TrackerClientProtocol()

    def clientConnectionFailed(self, connector, reason):
        print("[*] Connection failed: {}".format(reason))

    def clientConnectionLost(self, connector, reason):
        print("[*] Connection lost: {}".format(reason))


class TrackerClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        factory = TrackerClientFactory()
        reactor.connectTCP(host, port, factory)
