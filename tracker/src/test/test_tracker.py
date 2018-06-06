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
import uuid
import sys
import hashlib
# from unittest import mock
from twisted.trial import unittest
from twisted.test import proto_helpers
from twisted.internet import defer
from p2pchat.tracker import TrackerFactory
from p2pchat.database import P2PChatDB


class CreateChatTestCase(unittest.TestCase):

    def setUp(self):
        # TODO mock the database
        # TODO load these values from config?
        self.db = P2PChatDB("localhost", 0, "keyfile", "certfile")
        # self.db = P2PChatDB("localhost", 27017, "/etc/ssl/mongodb-cert.key", "/etc/ssl/mongodb-cert.crt")
        # self.db.connect()
        factory = TrackerFactory(self.db)
        self.proto = factory.buildProtocol()
        self.tr = proto_helpers.StringTransport()
        self.proto.makeConnection(self.tr)

    # @mock.patch.object(P2PChatDB, 'create_chat', autospec=True)
    def test_create_chat(self): 
        # Mock create_chat
        self.create_chat_called = False

        @defer.inlineCallbacks
        def fake_create_chat(chatuuid):
            self.create_chat_called = True
            result = yield {"5a6de3e8d6ca3f0fbd009af6"}
            defer.returnValue(result)

        self.db.create_chat = fake_create_chat
        # self.patch(self.db, "create_chat", fake_create_chat)
        createchat_json = {
            "action": "createchat",
        }

        createchat_str = json.dumps(createchat_json)
        self.proto.dataReceived(createchat_str)

        self.assertTrue(self.create_chat_called)
        # mock_create_chat.assert_called_once()

        createchat_response = self.tr.value()
        createchat_json = json.loads(createchat_response)
        self.assertTrue("chatuuid" in createchat_json)
        try:
            uuid.UUID(createchat_json["chatuuid"])
        except ValueError:
            self.fail("The chatuuid is not valid")

    # @mock.patch.object(P2PChatDB, 'store_message', autospec=True)
    def test_send_message(self):
        fake_msg_hash = str(hashlib.sha256(b"fake").hexdigest())
        fake_chatuuid = str(uuid.uuid4())
        sendmsg_json = {
            "action": "sendmessage",
            "chatuuid": fake_chatuuid,
            "msg_hash": fake_msg_hash
        }

        self.store_message_called = False

        @defer.inlineCallbacks
        def fake_store_message(chatuuid, msghash):
            self.store_message_called = True
            result = yield {"5a6de3e8d6ca3f0fbd009af6"}
            defer.returnValue(result)

        self.db.store_message = fake_store_message

        sendmsg_str = json.dumps(sendmsg_json)
        self.proto.dataReceived(sendmsg_str)
        # mock_send_message.assert_called_once()
        self.assertTrue(self.store_message_called)

        response = self.tr.value()
        try:
            response_json = json.loads(response)
        except:
            self.fail("sendmessage response is not valid JSON")

    # #@mock.patch.object(P2PChatDB, 'get_messages', autospec=True)
    # def test_get_messages(self, mock_get_messages):
    def test_get_messages(self):

        self.get_messages_called = False

        @defer.inlineCallbacks
        def fake_get_messages(chatuuid, fromtime):
            self.get_messages_called = True
            messages = yield {"foo": "bar"}
            defer.returnValue(messages)

        self.db.get_messages = fake_get_messages

        fakechatuuid = str(uuid.uuid4())
        getmessages_json = {
            "action": "getmessages",
            "chatuuid": fakechatuuid,
            "fromtime": 0
        }
        getmessages_str = json.dumps(getmessages_json)

        self.proto.dataReceived(getmessages_str)

        self.assertTrue(self.get_messages_called)

        response = self.tr.value()
        # TODO validate response
