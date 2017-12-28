#!/usr/bin/env python3

"""
The p2p connection frontend
"""

from kademlia.network import Server
import hashlib


class p2pConnection:

    def __init__(self, bootstrapAdresses):
        self.server = Server()
        self.server.listen(8468)  # Dynamic port range: 49152-65535

        self.server.bootstrap(bootstrapAdresses).addErrback(None)  # TODO: handle error in bootstrap

    def send(self, message):
        m = hashlib.sha256()
        m.update(message.to_bytes())
        key = m.hexdigest()
        self.server.set(key, message).addErrback(sendFailed)  # TODO: handle error in setting message

    def sendFailed(self, err):
        # Auto resend to network or ask user to resend?
        return None

    def get(self, key):
        message = self.server.get(key).addErrback(None)  # TODO: handle error in getting message
        return message

    def quit(self):
        return None
