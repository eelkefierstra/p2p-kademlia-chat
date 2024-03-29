#!/usr/bin/env python3

"""
The p2p connection frontend
"""

import os
import json
import hashlib
import logging
from kademlia.network import Server
from twisted.internet import asyncioreactor
import asyncio
from twisted.internet.defer import Deferred
from asyncio.tasks import ensure_future
# asyncioreactor.install(eventloop=loop)


class P2PConnection:

    def __init__(self, listenPort):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        log = logging.getLogger('kademlia')
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)

        self.loop = asyncio.get_event_loop()
        self.loop.set_debug(True)
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
        def done(res, key):
            print("Stored key:'{}' in network".format(key))
        d = self._send(key, chat_info_str)
        d.addCallback(done, key)
        d.addErrback(self.send_failed)
        return d


    def get_chat_info(self, chatuuid):
        d = self.get(chatuuid)
        return d

    def _send(self, key, data):
        print("Start storing key:'{}' in P2P-network".format(key))
        fut = ensure_future(self.server.set(key, data))
        d = Deferred.fromFuture(fut)
        # from twisted.internet import reactor
        # d.addTimeout(30, reactor, self.send_failed)
        return d

    def send(self, message):
        key = self.get_key(message)
        d = self._send(key, message)
        return d, key

    def send_failed(self, err):
        #TODO: Auto resend to network or ask user to resend?
        err.trap(TimeoutError)
        print('P2P send timed out')

    def get(self, key):
        fut = ensure_future(self.server.get(key))
        d = Deferred.fromFuture(fut)
        return d
