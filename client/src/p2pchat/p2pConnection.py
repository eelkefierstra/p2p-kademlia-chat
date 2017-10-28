#!/usr/bin/env python3

"""
The p2p connection frontend
"""

from kademlia.network import server

class p2pConnection:

    def __init__(self, bootstrapAdresses):
        self.server = Server()
        self.server.listen(50042) #Dynamic port range: 49152–65535

        for addres in bootstrapAdresses:
            self.server.bootstrap(addres).addErrback(none) #TODO: handle error in bootstrap

    def send(self, message):
        key = 'Test' #TODO: hash message to get key to safe message to
        self.server.set(key, message).addErrback(sendFailed) #TODO: handle error in setting message

    def sendFailed(err):
        #Auto resend to network or ask user to resend?

    def get(self, key):
        message = self.server.get(key).addErrback(none) #TODO: handle error in getting message
        return message

    def quit():
        
