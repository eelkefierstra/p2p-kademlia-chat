#!/usr/bin/env python3

"""
The p2p connection frontend
"""

import os
import json
import hashlib
from kademlia.network import Server
from twisted.internet import asyncioreactor
import asyncio
from twisted.internet.defer import Deferred
from asyncio.tasks import ensure_future
# asyncioreactor.install(eventloop=loop)


class P2PConnection:

    def __init__(self, listenPort):
        self.loop = asyncio.get_event_loop()
        asyncioreactor.install(eventloop=self.loop)
        
        self.server = Server()
        self.server.listen(listenPort)
        
        
    def connect_p2p(self, bootstrap_address):
        future = ensure_future(self.server.bootstrap([(bootstrap_address, 8468)]))
        d = Deferred.fromFuture(future)
        return d

    def get_key(self, content):
        return hashlib.sha256(str.encode(content)).hexdigest()

    def set_chat_info(self, chatuuid, groupname):
        chat_info = {
                    "name": groupname
                }
        chat_info_str = json.dumps(chat_info)
        key = chatuuid
        self._send(key, chat_info_str)

    def get_chat_info(self, chatuuid):
        d = self.get(chatuuid)
        return d

    def _send(self, key, data):
        def done():
            print("Stored key:'{}' in network".format(key))
            
        print("Start storing key:'{}' in P2P-network".format(key))
        fut = self.server.set(key, data)
        d = Deferred.fromFuture(fut)
        d.addCallback(done)
        d.addErrback(self.send_failed)

    def send(self, message):
        key = self.get_key(message)
        self._send(key, message)
        return key

    def send_failed(self, err):
        #TODO: Auto resend to network or ask user to resend?
        return

    def get(self, key):
        fut = self.server.get(key)
        d = Deferred.fromFuture(fut)
        return d
