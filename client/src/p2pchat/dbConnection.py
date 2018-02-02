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
                self.dbpool.runOperation("CREATE TABLE chats (id INTEGER PRIMARY KEY, chatName text, chatuuid text)")
                self.dbpool.runOperation("CREATE TABLE messages (chatHash text, chatContent text)")
                self.dbpool.runOperation("CREATE TABLE p2pMessageInfo (id INTEGER PRIMARY KEY, chatHash text, timeSend real, chatuuid text)")
            except:
                print('Error in creating tables')
                raise 'Database table creation error'
        return

    # Returns list of all connected chats
    def get_chat_list(self):
        try:
            return self.dbpool.runInteraction(self._get_chat_list)
        except:
            return None
    
    def _get_chat_list(self, txn):
        txn.execute("SELECT chatName, chatuuid FROM chats")
        result = txn.fetchall()
        if result:
            return [(chat[0], chat[1]) for chat in result]
        else:
            return None
    
    def insert_new_chat(self, chatName, chatuuid):
        try:
            self.dbpool.runOperation("INSERT INTO chats (chatName, chatuuid) VALUES (?,?)", [chatName, chatuuid])
        except:
            print('Error in inserting new chat')
            # TODO actually work around the error
    
    def delete_chat(self,chatName, chatuuid):
        return self.dbpool.runOperation("DELETE FROM chats WHERE chatName=? AND chatuuid=?", [chatName, chatuuid])
    
    def get_message(self, messageHash):
        return self.dbpool.runQuery("SELECT messageContent FROM messages WHERE messageHash=?", [messageHash])
    
    def get_chat_messages(self, chatuuid):
        return self.dbpool.runQuery("SELECT m.chatContent FROM p2pMessageInfo AS p, messages AS m WHERE p.chatuuid=? AND p.chatHash=m.chatHash ORDER BY p.timeSend ASC", [chatuuid])
    
    def insert_message(self, messageHash, messageContent, messageTime):
        # Check if message already stored
        return self.dbpool.runInteraction(self._insert_message, messageHash, messageContent, messageTime)
    
    def _insert_message(self, txn, messageHash, messageContent, messageTime, chatuuid):
        txn.execute("SELECT 1 FROM p2pMessageInfo WHERE messageHash=? AND timeSend=? AND chatuuid=?", [messageHash, messageTime, chatuuid])
        result = txn.fetchAll()
        if result:
            # This message send at this time is already saved, no point in doubling it
            return
        else:
            txn.execute("INSERT INTO p2pMessageInfo (?, ?, ?)", [messageHash, messageTime, chatuuid])
            
            # If content not yet stored store that in DB
            txn.execute("SELECT 1 FROM messages WHERE messageHash=?", [messageHash])
            result = txn.fetchAll()
            if result:
                # Content is already saved, continue
                return
            else:
                txn.execute("INSERT INTO messages (?, ?)", [messageHash, messageContent])
        return
    
    def __del__(self):
        self.dbpool.close()
        return
