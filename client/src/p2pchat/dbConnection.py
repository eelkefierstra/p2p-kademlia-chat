#!/usr/bin/env python3
'''
@author: Eelke
Connection to local sqlite DB
'''

from twisted.enterprise import adbapi


class dbConnection():
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('sqlite3', 'storage.db', check_same_thread=False)
        self.checkTableExistence('chats').addCallback(self.initTables)
        return
    
    # Checks if table exists in DB and return tablename in result[0][0]
    def checkTableExistence(self, tableName):
        return self.dbpool.runQuery("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [tableName])

    def initTables(self, checkResult):
        if checkResult:
            return
        else:
            try:
                # table does not exist, so we should create it
                self.dbpool.runOperation("CREATE TABLE chats (id INTEGER PRIMARY KEY, chatName text, chatUUID text)")
                self.dbpool.runOperation("CREATE TABLE messages (chatHash text, chatContent text)")
            except:
                print('Error in creating tables')
        return

    # Returns list of all connected chats
    def getChatList(self):
        try:
            return self.dbpool.runInteraction(self._getChatList)
        except:
            return None
    
    def _getChatList(self, txn):
        txn.execute("SELECT chatName FROM chats")
        result = txn.fetchall()
        if result:
            return [chat[0] for chat in result]
        else:
            return None
    
    def insertNewChat(self, chatName, chatUUID):
        try:
            self.dbpool.runOperation("INSERT INTO chats (chatName, chatUUID) VALUES (?,?)", [chatName, chatUUID])
        except:
            print('Error in inserting new chat')
    
    def deleteChat(self,chatName, chatUUID):
        return self.dbpool.runOperation("DELETE FROM chats WHERE chatName=? AND chatUUID=?", [chatName, chatUUID])
    
    def getMessage(self, messageHash):
        return self.dbpool.runQuery("SELECT messageContent FROM messages WHERE messageHash=?", [messageHash])
    
    def insertMessage(self, messageHash, messageContent):
        # Check if message already stored
        return self.dbpool.runInteraction(self._insertMessage, messageHash, messageContent)
    
    def _insertMessage(self, txn, messageHash, messageContent):
        txn.execute("SELECT 1 FROM messages WHERE messageHash=?", [messageHash])
        result = txn.fetchAll()
        if result:
            return
        else:
            txn.execute("INSERT INTO messages (?, ?)", [messageHash, messageContent])
        return
    
    def __del__(self):
        self.dbpool.close()
        return
