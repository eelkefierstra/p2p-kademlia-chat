'''
@author: Eelke
Interface for UI to communicate to core
'''


class uiInterface():
    def __init__(self, p2pObject, trackerObject):
        self.p2p = p2pObject
        self.tracker = trackerObject

    def createChat(self, name):
        # TODO: Send joined message to p2p
        # TODO: Notify tracker
        return
    
    def removeChat(self):
        # TODO: Only send left chat message?
        return
    
    def sendChatMessage(self, chat, message):
        # TODO: send message to p2p
        # TODO: send message hash to tracker
        return
