#!/usr/bin/env python3
"""
Unit tests for the tracker client.

Call this from the src folder with:
python3 -m twisted.trial test.test_trackerclient

For testing code coverage, run this with 
python3 -m twisted.trial --coverage test.test_trackerclient

For more info about the switches, please check out the twisted.trial docs.
"""

from twisted.trial import unittest
from twisted.test import proto_helpers
from p2pchat.trackerclient import TrackerClientFactory
import json
import uuid

class MessageUpdateTestCase(unittest.TestCase):

    def setUp(self):
        factory = TrackerClientFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def test_parse_new_chat(self): 
        chatuuid = uuid.uuid4()
        chatresponse_json = {
            "action" : "createchat",
            "chatuuid" : str(chatuuid)
        }
        chatresponse = json.dumps(chatresponse_json)
        self.proto.dataReceived(chatresponse)
