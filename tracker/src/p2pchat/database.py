#!/usr/bin/env python3

from OpenSSL import SSL
from txmongo.connection import ConnectionPool
from twisted.internet import defer, reactor, ssl
import datetime


class P2PChatDB(object):

    class ServerTLSContext(ssl.DefaultOpenSSLContextFactory):
        def __init__(self, *args, **kw):
            kw['sslmethod'] = SSL.TLSv1_METHOD
            ssl.DefaultOpenSSLContextFactory.__init__(self, *args, **kw)

    def __init__(self, host, port, privkey, certfile):
        self.host = host
        self.port = port
        self.privkey = privkey
        self.certfile = certfile

    def connect(self):
        tls_ctx = self.ServerTLSContext(privateKeyFileName=self.privkey, certificateFileName=self.certfile)
        self.db = yield ConnectionPool(self.host, self.port, ssl_context_factory=tls_ctx)

    @defer.inlineCallbacks
    def create_chat(self, chatuuid):
        self.db.p2pchat.groupchats.insert({"uuid" : chatuuid, "messages": []})

    @defer.inlineCallbacks
    def store_message(self, chatuuid, msghash):
        self.db.p2pchat.groupchats.update(
                {"uuid" : chatuuid},
                {"$push": 
                    {
                        "messages": {
                            "hash": msghash, 
                            "time": time.time()
                        }
                    }
                }
            )

    @defer.inlineCallbacks
    def get_messages(self, chatuuid, fromtime):
        messages = yield self.db.p2pchat.groupchats.find(
                    { "uuid" : chatuuid,
                      "messages" : { 
                          "$elemMatch" : {
                                "time" : {
                                    "$gt": fromtime
                                }
                            }
                        }
                    }
        
                )
        defer.returnValue(messages)
