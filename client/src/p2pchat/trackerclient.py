#!/usr/bin/env python3

"""
The p2p tracker client
"""

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import NetstringReceiver
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor
import json


class TrackerClientProtocol(NetstringReceiver):

    def __init__(self, factory):
        self.factory = factory

    def write_json(self, json_obj):
        response = json.dumps(json_obj)
        #self.transport.write(response.encode('utf-8'))
        self.sendString(response.encode('utf-8'))

    def create_chat(self):
        createchat_json = {
                "action"  : "createchat"
        }
        # TODO use second callback instead
        self.write_json(createchat_json)

    def send_message(self, chatuuid, msg_hash):
        sendmsg_json = {
            "action" : "sendmessage",
            "chatuuid" : chatuuid,
            "msg_hash" : msg_hash
        }
        self.write_json(sendmsg_json)

    """
    @param fromtime Receive messages after fromtime (unix timestamp utc)
    """
    def get_messages(self, chatuuid, fromtime):
        getmessages_json = {
                "action" : "getmessages",
                "chatuuid" : chatuuid,
                "fromtime" : str(fromtime)
        }
        self.write_json(getmessages_json)

        
        

    def parse_new_chat(self, chatJSON):
        chatuuid = chatJSON["chatuuid"]
        # TODO do something with this new chatuuid
        #print("[*] Created new chat with uuid: {}".format(chatuuid))
        #TODO use callback
        self.factory.notifier.on_chat_created(chatuuid)


    def parse_message_sent(self, msgJSON):
        chatuuid = msgJSON["chatuuid"]
        msg_hash = msgJSON["msg_hash"]
        self.factory.notifier.on_message_sent(chatuuid, msg_hash)

    def parse_messages(self, messagesJSON):
        # TODO if fromtime >= lastmsg_time, we missed some messages.
        # get the messages from lastmsg_time till fromtime also
        chatuuid = messagesJSON["chatuuid"]
        fromtime = messagesJSON["fromtime"]
        # TODO update the newest chat message time
        tilltime = messagesJSON["tilltime "]
        messages = messagesJSON["messages"]
        self.factory.notifier.on_messages_received(chatuuid, fromtime, tilltime, messages)

    def stringReceived(self, string):
        dataJSON = json.loads(string)
        action = dataJSON["action"]
        if action == "createdchat":
            # Created new chat
            self.parse_new_chat(dataJSON)
        elif action == "gotmessages":
            # New message locations arrived
            self.parse_messages(dataJSON)
        elif action == "sentmessage":
            self.parse_message_sent(dataJSON)

class ITrackerNotifier(object):

    def on_chat_created(self, chatuuid):
        """
        Called when a chat is created

        """

    def on_message_sent(self, chatuuid, msg_hash):
        """
        Called when a message is sent to the tracker
        """

    def on_messages_received(self, chatuuid, fromtime, tilltime, messages):
        """
        Called when messages are received from the tracker
        """


class TrackerClientFactory(ClientFactory):

    def __init__(self, notifier=ITrackerNotifier()):
        self.lastmsg_time = 0
        self.notifier = notifier

    def buildProtocol(self, addr):
        return TrackerClientProtocol(self)

    def clientConnectionFailed(self, connector, reason):
        print("[*] Connection failed: {}".format(reason))

    def clientConnectionLost(self, connector, reason):
        print("[*] Connection lost: {}".format(reason))



class TrackerClient:

    def __init__(self, host, port, notifier=ITrackerNotifier()):
        self.host = host
        self.port = port
        self.factory = TrackerClientFactory(notifier)

    def connect(self):
        endpoint = TCP4ClientEndpoint(reactor, self.host, self.port)
        return endpoint.connect(self.factory)

        #protocol = None
        #def prot_connected(prot):
        #    protocol = prot

        #d.addCallback(prot_connected)
        #return protocol

        #reactor.connectTCP(self.host, self.port, self.factory)
        #return self.factory.buildProtocol((self.host, self.port))
