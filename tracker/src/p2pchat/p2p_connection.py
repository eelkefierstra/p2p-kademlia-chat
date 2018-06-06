#!/usr/bin/env python3

from kademlia.network import Server
from twisted.internet import asyncioreactor
import asyncio
loop = asyncio.get_event_loop()
asyncioreactor.install(eventloop=loop)


class P2PConnection(object):
    '''
    Class for comunication with the p2p Kademlia network
    '''

    def __init__(self):
        self.server = Server()
        self.server.listen(8468)
