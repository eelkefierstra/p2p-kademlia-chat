'''
@author: Eelke
Interface for UI to communicate to core
'''
from twisted.internet.defer import inlineCallbacks
from p2pchat.trackerclient import ITrackerNotifier
import p2pchat.application
from tkinter import *
from twisted.internet import tksupport, reactor


class UIInterface(ITrackerNotifier):
    def __init__(self, p2pObject, trackerObject, dbConnection):
        self.p2p = p2pObject
        self.tracker = trackerObject
        self.dbConn = dbConnection
        
        root = Tk()
        # This fixes the reactor error on closing root window with the 'X' button
        root.protocol("WM_DELETE_WINDOW", reactor.stop)
        self.gui = p2pchat.application.Application(root, self)
        self.gui.master.title('Independed chat')
        tksupport.install(root)
        
        d = self.tracker.connect()
        d.addCallback(self.tracker_connected)
        
    def tracker_connected(self, proto):
        self.protocol_tracker = proto
    
    
    def create_chat(self, name):
        def chat_created(self, uuid):
            self.dbConn.insertNewChat(chatnameStr, uuid)
        try:
            chatnameStr = str(name)
            d = self.proto.create_chat(chatnameStr)
            d.callback(chat_created)
            
        except:
            # Could not make a string from message input
            # If you get here, you done something very wrong!!!
            print('error in creating chat')
        return
    
    def remove_chat(self):
        messagehash = self.p2p.send('User left chat.')
        self.dbConn.deleteChat(chatName, chatUUID) # Who knows UUID??????????
        # TODO: Only send left chat message?
        return
    
    def send_chat_message(self, chat, message, chatUUID):
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
    
    def get_chat_list(self):
        return self.dbConn.get_chat_list()
    
    # Callback point from tracker
    def on_chat_created(self):
        # TODO
        return
    
    # Callback point from tracker
    def on_message_sent(self):
        # TODO
        return
