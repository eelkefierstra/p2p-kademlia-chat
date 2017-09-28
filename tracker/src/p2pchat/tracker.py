#!/usr/bin/env python3

"""
The tracker server
"""

from twisted.internet.protocol import ServerFactory, Protocol

class TrackerProtocol(Protocol):
    
    def connectionMade(self):
        self.transport.write(self.factory.hellomsg)
        self.transport.loseConnection()

class TrackerFactory(ServerFactory):
    
    protocol = TrackerProtocol

    def __init__(self, hellomsg):
        self.hellomsg = hellomsg

class Tracker: 

    def __init__(self, iface, port):
        self.interface = iface
        self.port = port

    def start(self):
        hellomsg = "Hello World!".encode('utf-8')
        factory = TrackerFactory(hellomsg)
        from twisted.internet import reactor

        port = reactor.listenTCP(self.port, factory, interface=self.interface)

        reactor.run()


