#!/usr/bin/env python3
'''
@author: Eelke
Connection to local sqlite DB
'''

from twisted.enterprise import adbapi


class dbConnection():
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('sqlite3', 'storage.db')
        checkTableExistence('connectedChats').addCallback(initTables)
        return
    
    # Checks if table exists in DB and return tablename in result[0][0]
    def checkTableExistence(self, tableName):
        return self.dbpool.runQuery("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [tableName])

    def initTables(self, checkResult):
        if checkResult:
            if checkResult[0][0]=='connectedChats':
                return
            else:
                raise 'initTables called with wrong table'
        else:
            # table does not exist, so we should create it
            self.dbpool.execute("CREATE TABLE connectedChats (id INTEGER PRIMARY KEY, chatName text, chatUUID text)")
        return

    # Returns list of all connected chats
    def getChatList(self):
        return self.dbpool.runInteraction(_getChatList)
    
    def _getChatList(self, txn):
        txn.execute("SELECT chatName FROM connectedChats")
        result = txn.fetchAll()
        if result:
            return result[0]
        else:
            return None
