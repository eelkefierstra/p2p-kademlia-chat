#!/usr/bin/env python3

import argparse
import p2pchat.trackerclient
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

    root = Tk()
    gui = p2pchat.application.Application(root)
    gui.master.title('Independed chat')
    tksupport.install(root)

    for i in range(15):
        gui.addChat('chat'+str(i))

    trackerclient = p2pchat.trackerclient.TrackerClient(args.host, args.port)

    reactor.run()


if __name__ == "__main__":
    main()
