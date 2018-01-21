#!/usr/bin/env python3

import argparse
import p2pchat.trackerclient
import p2pchat.p2pConnection
import p2pchat.uiInterface
import p2pchat.application
from Tkinter import *
from twisted.internet import tksupport, reactor


def parse_args():
    description = """
This is the client for the p2p kademlia chat protoco=description
"""

    parser = argparse.ArgumentParser(description=description)

    helpPort = "The port to connect to. Default to 1337."
    parser.add_argument('--port', type=int, help=helpPort, default=1337)

    helpHost = "The host to connect to."
    parser.add_argument('--host', help=helpHost, default='127.0.0.1')

    args = parser.parse_args()
    print(args)

    return args


def main():
    args = parse_args()

    trackerclient = p2pchat.trackerclient.TrackerClient(args.host, args.port)
    # TODO: get bootstrapaddresses
    p2p = p2pchat.p2pConnection.p2pConnection(args.host)

    uiinterface = p2pchat.uiInterface.uiInterface(p2p, trackerclient)

    root = Tk()
    gui = p2pchat.application.Application(root, uiinterface)
    gui.master.title('Independed chat')
    tksupport.install(root)

    # TODO: remove testcode before final version
    for i in range(15):
        gui.addChat('chat'+str(i))


    reactor.run()


if __name__ == "__main__":
    main()
