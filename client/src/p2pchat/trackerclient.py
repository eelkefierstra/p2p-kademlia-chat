#!/usr/bin/env python3

"""
The p2p tracker client
"""

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import NetstringReceiver
from twisted.internet.endpoints import TCP4ClientEndpoint
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

    #def request_push_notifications(self, chatuuids):
    #    push_request_json = {
    #        "action": "get_notified",
    #        "chats": chatuuids
    #    }
    #    self.write_json(push_request_json)

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
            "fromtime" : fromtime
        }
        self.write_json(getmessages_json)

    def receive_notifications(self, chatuuids):
        getnotified_json = {
            "action": "get_notified",
            "chats": chatuuids
        }
        self.write_json(getnotified_json)



    def parse_new_chat(self, chatJSON):
        chatuuid = chatJSON["chatuuid"]
        self.factory.notifier.on_chat_created(chatuuid)


    def parse_message_sent(self, msgJSON):
        print("Message sent data received")
        chatuuid = msgJSON["chatuuid"]
        msg_hash = msgJSON["msg_hash"]
        time_sent = msgJSON["time_sent"]
        self.factory.notifier.on_message_sent(chatuuid, msg_hash, time_sent)

    def parse_message(self, messageJSON):
        chatuuid = messageJSON["chatuuid"]
        msg_hash = messageJSON["msg_hash"]
        time_sent = messageJSON["time_sent"]
        self.factory.notifier.on_message_received(chatuuid, msg_hash, time_sent)



    def parse_messages(self, messagesJSON):
        # TODO if fromtime >= lastmsg_time, we missed some messages.
        # get the messages from lastmsg_time till fromtime also
        chatuuid = messagesJSON["chatuuid"]
        fromtime = messagesJSON["fromtime"]
        # TODO update the newest chat message time
        tilltime = messagesJSON["tilltime"]
        messages = messagesJSON["messages"]
        self.factory.notifier.on_messages_received(chatuuid, fromtime, tilltime, messages)

    def stringReceived(self, string):
        try:
            dataJSON = json.loads(string.decode('utf-8'))
        except UnicodeError:
            # discard input which is not
            print("Can't decode to utf-8, discarding input.", file=sys.stderr)
            return
        except json.JSONDecodeError:
            print("Can't decode JSON, discarding input.", file=sys.stderr)
            return

        action = dataJSON["action"]
        if action == "createdchat":
            # Created new chat
            self.parse_new_chat(dataJSON)
        elif action == "gotmessage":
            # Got new message location
            self.parse_message(dataJSON)
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

    def on_message_sent(self, chatuuid, msg_hash, time_sent):
        """
        Called when a message is sent to the tracker
        """

    def on_messages_received(self, chatuuid, fromtime, tilltime, messages):
        """
        Called when messages are received from the tracker
        """

    def on_message_received(self, chatuuid, msg_hash, time_sent):
        """
        Called when a message is pushed by the tracker
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
        from twisted.internet import reactor
        endpoint = TCP4ClientEndpoint(reactor, self.host, self.port)
        return endpoint.connect(self.factory)

        #protocol = None
        #def prot_connected(prot):
        #    protocol = prot

        #d.addCallback(prot_connected)
        #return protocol

        #reactor.connectTCP(self.host, self.port, self.factory)
        #return self.factory.buildProtocol((self.host, self.port))
