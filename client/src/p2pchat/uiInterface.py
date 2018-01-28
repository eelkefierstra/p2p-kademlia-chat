'''
@author: Eelke
Interface for UI to communicate to core
'''
from twisted.internet.defer import inlineCallbacks


class uiInterface:
    def __init__(self, p2pObject, trackerObject, dbConnection):
        self.p2p = p2pObject
        self.tracker = trackerObject
        self.dbConn = dbConnection

    def createChat(self, name):
        try:
            chatnameStr = str(name)
            messageHash = self.p2p.send('User joined chat.')
            # TODO: Notify tracker
            self.dbConn.insertNewChat(chatnameStr, chatUUID)
        except:
            # Could not make a string from message input
            # If you get here, you done something very wrong!!!
            pass
        return
    
    def removeChat(self):
        messagehash = self.p2p.send('User left chat.')
        self.dbConn.deleteChat(chatName, chatUUID) # Who knows UUID??????????
        # TODO: Only send left chat message?
        return
    
    def sendChatMessage(self, chat, message):
        try:
            messageStr = str(message)
            messagehash = self.p2p.send(messageStr)
            # TODO: send message hash to tracker
            self.dbConn.insertMessage(messagehash, messageStr)
        except:
            # Could not make a string from message input
            # If you get here, you done something very wrong!!!
            pass
        return
    
    def getChatList(self):
        return self.dbConn.getChatList()
