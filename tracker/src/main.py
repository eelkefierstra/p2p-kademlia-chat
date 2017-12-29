#!/usr/bin/env python3

import optparse
import p2pchat.p2pConnection
import p2pchat.tracker


def parse_args():
    usage = """Usage: %prog [options]

This is the tracker server for the p2p kademlia chat protocol.

"""

    parser = optparse.OptionParser(usage)

    helpPort = "The port to listen on. Default to 1337."
    parser.add_option('--port', type='int', help=helpPort, default=1337)

    helpIface = "The interface to listen on. Default is localhost."
    parser.add_option('--iface', help=helpIface, default='localhost')

    options, args = parser.parse_args()

    return options


if __name__ == "__main__":
    options = parse_args()
    p2pServer = p2pchat.p2pConnection.p2pConnection()
    tracker = p2pchat.tracker.Tracker(options.iface, options.port)
    tracker.start()
