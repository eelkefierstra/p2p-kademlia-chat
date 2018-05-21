#!/usr/bin/env python3
'''
@author: Eelke
Connection to local sqlite DB
'''

from twisted.enterprise import adbapi
from twisted.internet import defer


class DBConnection():
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('sqlite3', 'storage.db', check_same_thread=False)

    def setup_db(self):
        d = self.init_tables()
        return d

    def init_tables(self):
        # table does not exist, so we should create it
        d_chats = self.dbpool.runOperation(
                """
                CREATE TABLE IF NOT EXISTS chats(
                    id INTEGER PRIMARY KEY,
                    chatName TEXT,
                    chatuuid TEXT,
                    last_msg_update INTEGER DEFAULT 0,
                    CONSTRAINT chatuuid_unique UNIQUE(chatuuid)
                );
                """
             )
        d_messages = self.dbpool.runOperation(
                """CREATE TABLE IF NOT EXISTS messages(
                       messageHash TEXT,
                       chatContent TEXT
                   );""")
        d_p2p_message_info = self.dbpool.runOperation(
                """CREATE TABLE IF NOT EXISTS p2pMessageInfo(
                       id INTEGER PRIMARY KEY,
                       messageHash text,
                       timeSend real,
                       chatuuid text
                   );""")
        dl = defer.DeferredList([d_chats,d_messages,d_p2p_message_info])
        return dl

    # Returns list of all connected chats
    def get_chat_list(self):
        try:
            d = self.dbpool.runInteraction(self._get_chat_list)
            return d
        except:
            return None

    def _get_chat_list(self, txn):
        txn.execute("SELECT chatName, chatuuid FROM chats")
        result = txn.fetchall()
        if result:
            info = [(chat[0], chat[1]) for chat in result]
            print("Got chats from DB: {}".format(info))
            return info
        else:
            return None

    def insert_new_chat(self, chatName, chatuuid):
        # runOperation returns a deferred
        return self.dbpool.runOperation("INSERT INTO chats (chatName, chatuuid) VALUES (?,?)", [chatName, chatuuid])

    def delete_chat(self,chatName, chatuuid):
        return self.dbpool.runOperation("DELETE FROM chats WHERE chatName=? AND chatuuid=?", [chatName, chatuuid])

    def get_latest_msg_ts(self, chatuuid):
        d = self.dbpool.runQuery("""
                    SELECT last_msg_update
                    FROM chats
                    WHERE chatuuid = ?;""", [chatuuid])
        # strip it, so select first result, first column
        d.addCallback(lambda result: result[0][0])
        return d

    def set_latest_msg_ts(self, chatuuid, ts):
        return self.dbpool.runOperation("""
                        UPDATE chats
                        SET last_msg_update = ?
                        WHERE chatuuid = ?;
                        """, [ts, chatuuid])


    def get_message(self, messageHash):
        return self.dbpool.runQuery("SELECT messageContent FROM messages WHERE messageHash=?", [messageHash])

    def get_chat_messages(self, chatuuid):
        return self.dbpool.runQuery("SELECT m.chatContent FROM p2pMessageInfo AS p, messages AS m WHERE p.chatuuid=? AND p.messageHash=m.messageHash ORDER BY p.timeSend ASC", [chatuuid])

    def insert_message(self, message_hash, message_content, message_time, chat_uuid):
        # Check if message already stored
        return self.dbpool.runInteraction(self._insert_message, message_hash, message_content, message_time, chat_uuid)

    def _insert_message(self, txn, message_hash, message_content, message_time, chat_uuid):
        txn.execute("SELECT 1 FROM p2pMessageInfo WHERE messageHash=? AND timeSend=? AND chatuuid=?", [message_hash, message_time, chat_uuid])
        result = txn.fetchall()
        if result:
            # This message send at this time is already saved, no point in doubling it
            return
        else:
            txn.execute("INSERT INTO p2pMessageInfo (messageHash, timeSend, chatuuid)  VALUES (?, ?, ?)", (message_hash, message_time, chat_uuid))
            print("Message added to DB")
            # If content not yet stored store that in DB
            txn.execute("SELECT 1 FROM messages WHERE messageHash=?", [message_hash])
            result = txn.fetchall()
            if result:
                # Content is already saved, continue
                return
            else:
                txn.execute("INSERT INTO messages (messageHash, chatContent) VALUES (?, ?)", [message_hash, message_content])
                print("Message content added to DB")
        return

    def __del__(self):
        self.dbpool.close()
        return
