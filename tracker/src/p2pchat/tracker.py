#!/usr/bin/env python3

"""
The tracker server
"""

import socket

class Tracker:
    
    def __init__(self,bindaddr):
        self.bindaddr = bindaddr
        self.clients = []

    def start(self):
        self.acceptconnections()

    def stop(self):
        self.serversock.close()

    def acceptconnections(self):
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversock.bind(self.bindaddr)
        self.serversock.listen(10)
        while True:
            clientconn, addr = self.serversock.accept()
            print("Started connection with {}".format(addr))
            self.clients.append(clientconn)
            clientconn.send(b"Hello from server")
