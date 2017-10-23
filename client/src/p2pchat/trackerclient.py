#!/usr/bin/env python3

"""
The p2p tracker client
"""

import socket

class TrackerClient:

    def __init__(self, trackeraddr):
        self.trackeraddr = trackeraddr

    def connect(self):
        self.trackerconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.trackerconn.connect(self.trackeraddr)
        self.trackerconn.send(b"Joined")
        servermsg = self.trackerconn.recv(1024)
        print(servermsg)

    def disconnect(self):
        self.trackerconn.send(b"Disconnect")
        self.trackerconn.close()
