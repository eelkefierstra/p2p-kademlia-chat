#!/usr/bin/env python3
"""
Unit tests for the tracker.

Call this from the src folder with:
python3 -m twisted.trial test.test_tracker

For testing code coverage, run this with
python3 -m twisted.trial --coverage test.test_tracker

For more info about the switches, please check out the twisted.trial docs.
"""

import json
from twisted.trial import unittest
from twisted.test import proto_helpers
from p2pchat.tracker import TrackerFactory
# TODO mock database?
# from p2pchat.database import P2PChatDB


class TestDB(object):
    def __init__(self):
        self.p2pchat = {
            "groupchats": {
            }
        }

    def create_chat(self, chatuuid):
        self.p2pchat["groupchats"][chatuuid] = chatuuid


class CreateChatTestCase(unittest.TestCase):

    def setUp(self):
        # TODO create the test client
        # TODO create the database connection, or mock it?
        db = TestDB()
        factory = TrackerFactory(db)
        self.proto = factory.buildProtocol()
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)
        # self.db = P2PChatDB(args.dbhost, args.dbport, args.dbprivkey, args.dbcert)
        # self.db.connect()

    def test_parse_new_chat(self): 
        createchat_json = {
            "action": "createchat",
        }
        createchat_str = json.dumps(createchat_json)
        self.proto.dataReceived(createchat_str)
