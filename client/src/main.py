#!/usr/bin/env python3

import optparse
import p2pchat.trackerclient

def parse_args():
    usage = """Usage: %prog [options]

This is the client for the p2p kademlia chat protocol.
"""

    parser = optparse.OptionParser(usage)

    help = "The port to connect to. Default to 1337."
    parser.add_option('--port', type='int', help=help, default=1337)

    help = "The host to connect to."
    parser.add_option('--host', help=help)

    options, args = parser.parse_args()

    return options



if __name__ == "__main__":
    options = parse_args()
    trackerclient = p2pchat.trackerclient.TrackerClient('localhost', 1337) 

