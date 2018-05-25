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
        d = self._send(key, chat_info_str)
        d.addCallback(done, key)
        d.addErrback(self.send_failed)
        return d
        
        def done(res, key):
            print("Stored key:'{}' in network".format(key))

    def get_chat_info(self, chatuuid):
        d = self.get(chatuuid)
        return d

    def _send(self, key, data):
        print("Start storing key:'{}' in P2P-network".format(key))
        fut = ensure_future(self.server.set(key, data))
        d = Deferred.fromFuture(fut)
        from twisted.internet import reactor
        d.addTimeout(30, reactor, self.send_failed)
        return d

    def send(self, message):
        key = self.get_key(message)
        self._send(key, message)
        return key

    def send_failed(self, err):
        #TODO: Auto resend to network or ask user to resend?
        if type(err) is TimeoutError:
            print('P2P send timed out')
        else:
            print(err)
        return

    def get(self, key):
        fut = ensure_future(self.server.get(key))
        d = Deferred.fromFuture(fut)
        return d
