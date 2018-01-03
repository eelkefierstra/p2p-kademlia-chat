#!/usr/bin/env python3

import argparse
import p2pchat.tracker

def parse_args():
    description = """
This is the tracker server for the p2p kademlia chat protocol.

"""

    parser = argparse.ArgumentParser(description=description)

    help = "The port to listen on. Default to a random available port."
    parser.add_argument('--port', type=int, help=help, default=1337)

    help = "The interface to listen on. Default is localhost."
    parser.add_argument('--iface', help=help, default='localhost')

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    tracker = p2pchat.tracker.Tracker(args.iface, args.port)
    tracker.start()
