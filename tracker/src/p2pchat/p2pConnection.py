'''
@author: Eelke
'''
import os
from kademlia.network import Server


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
        self.server.saveStateRegularly('cache.tmp', 10)
