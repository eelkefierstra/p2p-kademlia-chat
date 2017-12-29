#!/usr/bin/env python3

"""
The p2p connection frontend
"""

from kademlia.network import Server
import os
import hashlib


class p2pConnection:

    def __init__(self, bootstrapAdres):

        if os.path.isfile('cache.tmp'):
            self.server = Server.loadState('cache.tmp')
        else:
            self.server = Server()
            self.server.listen(8468)  # Dynamic port range: 49152-65535
            self.server.bootstrap([(bootstrapAdres, 8468)])
        self.server.saveStateRegularly('cache.tmp', 10)

    def send(self, message):
        m = hashlib.sha256()
        m.update(str.encode(message))
        key = m.hexdigest()
        self.server.set(key, message).addErrback(self.sendFailed)  # TODO: handle error in setting message

    def sendFailed(self, err):
        # Auto resend to network or ask user to resend?
        return None

    def get(self, key):
        message = self.server.get(key).addErrback(None)  # TODO: handle error in getting message
        return message

    def quit(self):
        return None
