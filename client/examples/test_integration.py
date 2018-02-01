#!/usr/bin/env python3
import sys
sys.path.append('../src/')
from p2pchat.trackerclient import TrackerClient, ITrackerNotifier
from twisted.internet import reactor, defer
import hashlib

class MyChatApp(ITrackerNotifier):
    
    def __init__(self):
        self.trackerclient = TrackerClient("localhost", 1337, notifier=self)

    def on_chat_created(self, chatuuid):
        print("[*] Created new chat with uuid: {}".format(chatuuid))
        d = defer.Deferred()
        d.addCallback(self.receive_notifications)
        def print_err(err):
            print(err)
        d.addErrback(print_err)
        d.addCallback(self.send_msg)
        d.addCallback(self.get_messages)
        d.callback(chatuuid)
        #self.chatuuid = chatuuid

    def on_message_sent(self, chatuuid, msg_hash):
        print("[*] Message sent: {} {}".format(chatuuid, msg_hash))

    def on_messages_received(self, chatuuid, fromtime, tilltime, messages):
        print("[*] Messages received: {} {} {} {}".format(chatuuid, fromtime, tilltime, messages))

    def on_message_received(self, chatuuid, msg_hash, time_sent):
        print("[*] Message received: {} {} {}".format(chatuuid, msg_hash, time_sent))

    def create_chat(self, protocol):
        self.protocol = protocol
        protocol.create_chat()

    def receive_notifications(self, chatuuid):
        chatuuids = [chatuuid]
        self.protocol.receive_notifications(chatuuids)
        return chatuuid

    def send_msg(self, chatuuid):
        # TODO supply hash
        print("[*] sending message ...")
        fakehash = str(hashlib.sha256(b"foo").hexdigest())
        self.protocol.send_message(chatuuid, fakehash)
        return chatuuid

    def get_messages(self, chatuuid):
        self.protocol.get_messages(chatuuid, 0)


    def start(self):
        d = self.trackerclient.connect()
        d.addCallback(self.create_chat)

        d.addBoth(lambda x: print("done"))
        #endpoint.create_chat()
        print("running...")
        reactor.run()

if __name__ == "__main__":

    #endpoint = TCP4ServerEndpoint(reactor, 8007)
    chatapp = MyChatApp()
    chatapp.start()
