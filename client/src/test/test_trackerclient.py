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
#import p2pchat.tracker as tracker
from p2pchat.trackerclient import TrackerClientFactory
import json
import uuid

class MessageUpdateTestCase(unittest.TestCase):

    def setUp(self):
        # TODO create the testtracker
        #trackerfactory = 
        # Create the client connection
        factory = TrackerClientFactory()
        self.proto = factory.buildProtocol(('127.0.0.1', 0))
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    def test_create_chat(self):
        self.proto.create_chat()
        request = self.tr.value()

        try:
            createchat_json = json.loads(request)
        except json.decoder.JSONDecodeError:
            self.fail("create_chat request is not valid json")
