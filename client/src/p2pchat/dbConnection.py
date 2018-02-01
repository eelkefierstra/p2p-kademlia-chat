#!/usr/bin/env python3
'''
@author: Eelke
Connection to local sqlite DB
'''

from twisted.enterprise import adbapi


class dbConnection():
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('sqlite3', 'storage.db', check_same_thread=False)
        self.check_table_existence('chats').addCallback(self.init_tables)
        return
    
    # Checks if table exists in DB and return tablename in result[0][0]
    def check_table_existence(self, tableName):
        return self.dbpool.runQuery("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [tableName])

    def init_tables(self, checkResult):
        if checkResult:
            return
        else:
            try:
                # table does not exist, so we should create it
                self.dbpool.runOperation("CREATE TABLE chats (id INTEGER PRIMARY KEY, chatName text, chatUUID text)")
                self.dbpool.runOperation("CREATE TABLE messages (chatHash text, chatContent text)")
                self.dbpool.runOperation("CREATE TABLE p2pMessageInfo (id INTEGER PRIMARY KEY, chatHash text, timeSend integer)")
            except:
                print('Error in creating tables')
        return

    # Returns list of all connected chats
    def get_chat_list(self):
        try:
            return self.dbpool.runInteraction(self._get_chat_list)
        except:
            return None
    
    def _get_chat_list(self, txn):
        txn.execute("SELECT chatName FROM chats")
        result = txn.fetchall()
        if result:
            return [chat[0] for chat in result]
        else:
            return None
    
    def insert_new_chat(self, chatName, chatUUID):
        try:
            self.dbpool.runOperation("INSERT INTO chats (chatName, chatUUID) VALUES (?,?)", [chatName, chatUUID])
        except:
            print('Error in inserting new chat')
    
    def delete_chat(self,chatName, chatUUID):
        return self.dbpool.runOperation("DELETE FROM chats WHERE chatName=? AND chatUUID=?", [chatName, chatUUID])
    
    def get_message(self, messageHash):
        return self.dbpool.runQuery("SELECT messageContent FROM messages WHERE messageHash=?", [messageHash])
    
    def insert_message(self, messageHash, messageContent):
        # Check if message already stored
        return self.dbpool.runInteraction(self._insert_message, messageHash, messageContent)
    
    def _insert_message(self, txn, messageHash, messageContent):
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
