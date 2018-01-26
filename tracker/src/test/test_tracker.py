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
    def test_create_chat(self, mock_create_chat): 
        createchat_json = {
            "action" : "createchat",
        }

        createchat_str = json.dumps(createchat_json)
        self.proto.dataReceived(createchat_str)

        mock_create_chat.assert_called_once()

        createchat_response = self.tr.value()
        createchat_json = json.loads(createchat_response)
        self.assertTrue("chatuuid" in createchat_json)
        try:
            uuid.UUID(createchat_json["chatuuid"])
        except ValueError:
            self.fail("The chatuuid is not valid")

        #print("create chat return value: {}".format(self.tr.value()))
        # TODO check response


    @mock.patch.object(P2PChatDB, 'store_message', autospec=True)
    def test_send_message(self, mock_send_message):
        fake_msg_hash = str(hashlib.sha256(b"fake").hexdigest())
        sendmsg_json = {
            "action" : "sendmessage",
            "chatuuid" : "<chatuuid>",
            "msg_hash" : fake_msg_hash
        }

        sendmsg_str = json.dumps(sendmsg_json)
        self.proto.dataReceived(sendmsg_str)

        mock_send_message.assert_called_once()

        response = self.tr.value()
        try:
            response_json = json.loads(response)
        except:
            self.fail("sendmessage response is not valid JSON")

        print(response_json)

    @mock.patch.object(P2PChatDB, 'get_messages', autospec=True)
    def test_get_messages(self, mock_get_messages):
        #mock_get_messages = mock.MagicMock()
        mock_get_messages.return_value = { "foo" : "bar" }
        #self.patch(self.db, "get_messages", mock_get_messages)
        getmessages_json = {
            "action" : "getmessages",
            "chatuuid" : "<chatuuid>",
            "fromtime" : 0
        }
        getmessages_str = json.dumps(getmessages_json)
        self.proto.dataReceived(getmessages_str)
        mock_get_messages.assert_called_once()
        


#class GetMessagesTestCase(unittest.TestCase):
#
#    def setUp(self):
#        self.db = P2PChatDB("localhost", 0, "", "")
#        factory = TrackerFactory(self.db)
#        self.proto = factory.buildProtocol()
#        self.tr = proto_helpers.StringTransport()
#        self.proto.makeConnection(self.tr)
#    
#    @mock.patch.object(P2PChatDB, 'get_messages', autospec=True)
#    def test_get_messages(self, mock_get_messages):
#        getmessages_json = {
#            "action" : "getmessages",
#            "chatuuid" : "<chatuuid>",
#            "fromtime" : 0
#        }
#        getmessages_str = json.dumps(getmessages_json)
#        self.proto.dataReceived(getmessages_str)
#        mock_get_messages.assert_called_once()
