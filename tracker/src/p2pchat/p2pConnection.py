'''
@author: Eelke
'''
import os
from kademlia.network import Server
from twisted.internet import reactor
import asyncio


class p2pConnection(object):
    '''
    Class for comunication with the p2p Kademlia network
    '''

    def __init__(self):
        if os.path.isfile('cache.tmp'):
            self.server = Server.loadState('cache.tmp')
        else:
            self.server = Server()
            self.server.listen(8468)
            self.loop = asyncio.get_event_loop()
            reactor.callInThread(self.start_p2p_loop)
        self.server.saveStateRegularly('cache.tmp', 10)

    def start_p2p_loop(self):
        self.loop.run_forever()

    def stop(self):
        self.server.stop()
        self.loop.close()

    def __del__(self):
        self.stop()
