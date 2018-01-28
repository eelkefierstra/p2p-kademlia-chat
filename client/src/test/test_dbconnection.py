#!/usr/bin/env python3
"""
Unit tests for the tracker client.

Call this from the src folder with:
python3 -m twisted.trial test.test_trackerclient

For testing code coverage, run this with 
python3 -m twisted.trial --coverage test.test_trackerclient

For more info about the switches, please check out the twisted.trial docs.
"""

from twisted.internet.defer import inlineCallbacks
from twisted.trial import unittest
from p2pchat.dbConnection import dbConnection
from tempfile import mkdtemp
from shutil import rmtree
from twisted.enterprise import adbapi
import os.path as osp

class databaseConnectionTestCase(unittest.TestCase):

    def setUp(self):
        self.tempfolder = mkdtemp()
        
        self.dbpool = adbapi.ConnectionPool('sqlite3', osp.join(self.tempfolder, 'storage.db'))
        self.dbpool.execute("CREATE TABLE chats (id INTEGER PRIMARY KEY, chatName text, chatUUID text)")
        self.dbpool.execute("CREATE TABLE messages (chatHash text, chatContent text)")
    
    def tearDown(self):
        self.dbpool.close()
        del self.dbpool
        rmtree(self.tempfolder)
    
    @inlineCallbacks
    def test_checkTableExistence(self):
        yield self.dbpool
        result = yield self.dbpool.runQuery("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [tableName])
        
        self.assertTrue()
        return
        
    def test_parse_new_chat(self): 
        return