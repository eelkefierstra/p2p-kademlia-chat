'''
@author: Eelke
Interface for UI to communicate to core
'''


class uiInterface:
    def __init__(self, p2pObject, trackerObject):
        self.p2p = p2pObject
        self.tracker = trackerObject

    def createChat(self, name):
        try:
            chatnameStr = str(name)
            messageHash = self.p2p.send('User joined chat.')
            # TODO: Notify tracker (in callback?)
        except:
            # Could not make a string from message input
            # If you get here, you done something very wrong!!!
            pass
        return
    
    def removeChat(self):
        messagehash = self.p2p.send('User left chat.')
        # TODO: Only send left chat message?
        return
    
    def sendChatMessage(self, chat, message):
        try:
            messageStr = str(message)
            messagehash = self.p2p.send(messageStr)
            # TODO: send message hash to tracker (In callback?)
        except:
            # Could not make a string from message input
            # If you get here, you done something very wrong!!!
            pass
        return
