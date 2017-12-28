#!/usr/bin/env python3

import optparse
import p2pchat.trackerclient
import p2pchat.p2pConnection
import p2pchat.application
from Tkinter import *
from twisted.internet import tksupport, reactor


def parse_args():
    usage = """Usage: %prog [options]

This is the client for the p2p kademlia chat protocol.
"""

    parser = optparse.OptionParser(usage)

    helpPort = "The port to connect to. Default to 1337."
    parser.add_option('--port', type='int', help=helpPort, default=1337)

    helpHost = "The host to connect to."
    parser.add_option('--host', help=helpHost, default='127.0.0.1')

    options, args = parser.parse_args()

    return options


def main():
    options = parse_args()

    root = Tk()
    gui = p2pchat.application.Application(root)
    gui.master.title('Independed chat')
    tksupport.install(root)

    for i in range(15):
        gui.addChat('chat'+str(i))

    trackerclient = p2pchat.trackerclient.TrackerClient(options.host, options.port)
    # TODO: get bootstrapaddresses
    p2p = p2pchat.p2pConnection.p2pConnection([options.host])
    p2p.send('Test message to test p2p network.')

    reactor.run()


if __name__ == "__main__":
    main()
