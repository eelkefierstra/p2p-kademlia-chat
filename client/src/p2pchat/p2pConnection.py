#!/usr/bin/env python3

"""
The p2p connection frontend
"""

from kademlia.network import Server
import os
import hashlib
from twisted.internet import defer
import asyncio
import json


class p2pConnection:

    def __init__(self, bootstrapAdres, listenPort):
        self.server = Server()
        self.server.listen(listenPort)
        
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.server.bootstrap([(bootstrapAdres, 8468)]))

    def get_key(self, content):
        return hashlib.sha256(content).hexdigest()

    def set_chat_info(self, chatuuid, groupname):
        chat_info = {
                    "name": groupname
                }
        chat_info_str = json.dumps(chat_info)
        key = chatuuid
        self._send(key, chat_info_str)

    def get_chat_info(self, chatuuid):
        key = chatuuid
        d = self.get(key)

        def got_chat_info(chat_info_str):
            chat_info = json.loads(chat_info_str)
            if "name" not in chat_info:
                d.errback(TypeError("Chatname is not in chat_info"))
            return chat_info

        d.addCallback(got_chat_info)
        return d

    def _send(self, key, message):
        self.loop.run_until_complete(self.server.set(key, message))  # TODO: handle error in setting message

    def send(self, message):
        key = self.get_key(message)
        self._send(key, message)
        return key

    def sendFailed(self, err):
        # Auto resend to network or ask user to resend?
        return

    def get(self, key):
        try:
            message = self.loop.run_until_complete(self.server.get(key))
        except:
            # TODO: Could not get message from network, what now?
            return
        return message
