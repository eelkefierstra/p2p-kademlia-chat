#!/usr/bin/env python3

from twisted.trial import unittest
from twisted.test import proto_helpers
from p2pchat.tracker import TrackerFactory

class CreateChatTestCase(unittest.TestCase):

    def setUp(self):
        #TODO create the test client
        #TODO create the database connection, or mock it?
        factory = TrackerFactory(db)
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)


    def test_parse_new_chat(self): 
        createchat_json = {
            "action" : "createchat",
        }
        createchat_str = json.dumps(createchat_json)
        self.proto.dataReceived(createchat_str)
