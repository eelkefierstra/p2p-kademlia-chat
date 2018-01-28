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
import hashlib

class MessageUpdateTestCase(unittest.TestCase):

    def setUp(self):
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

        self.assertTrue("action" in createchat_json)

    def test_send_message(self):
        fakeuuid = str(uuid.uuid4())
        fakehash = str(hashlib.sha256(b"foo").hexdigest())
        self.proto.send_message(fakeuuid, fakehash)
        
        send_request = self.tr.value()
        try:
            send_request_json = json.loads(send_request)
        except json.decoder.JSONDecodeError:
            self.fail("send_message request is not valid json")

        self.assertTrue("chatuuid" in send_request_json)
        self.assertTrue("action" in send_request_json)
        self.assertTrue("msg_hash" in send_request_json)

    def test_get_messages(self):
        fakeuuid = str(uuid.uuid4())
        fromtime = 0
        self.proto.get_messages(fakeuuid, fromtime)
        getmessages_request = self.tr.value()

        try:
            getmessages_json = json.loads(getmessages_request)
        except json.decoder.JSONDecodeError:
            self.fail("send_message request is not valid json")

        self.assertTrue("chatuuid" in getmessages_json)
        self.assertTrue("action" in getmessages_json)
        self.assertTrue("fromtime" in getmessages_json)

