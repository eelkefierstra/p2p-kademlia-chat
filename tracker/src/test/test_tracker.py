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
from unittest import mock
from twisted.trial import unittest
from twisted.test import proto_helpers
from p2pchat.tracker import TrackerFactory
from p2pchat.database import P2PChatDB

class CreateChatTestCase(unittest.TestCase):

    def setUp(self):
        self.db = P2PChatDB("localhost", 0, "", "")
        factory = TrackerFactory(self.db)
        self.proto = factory.buildProtocol()
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    @mock.patch.object(P2PChatDB, 'create_chat', autospec=True)
    def test_parse_new_chat(self, mock_create_chat): 
        createchat_json = {
            "action" : "createchat",
        }
        createchat_str = json.dumps(createchat_json)
        self.proto.dataReceived(createchat_str)
        mock_create_chat.assert_called_once()

