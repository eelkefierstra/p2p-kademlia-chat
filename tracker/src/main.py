#!/usr/bin/env python3

import optparse
import p2pchat.tracker

def parse_args():
    usage = """usage: %prog [options]

This is the Fast Poetry Server, Twisted edition.
Run it like this:

  python main.py
"""

    parser = optparse.OptionParser(usage)

    help = "The port to listen on. Default to a random available port."
    parser.add_option('--port', type='int', help=help, default=1337)

    help = "The interface to listen on. Default is localhost."
    parser.add_option('--iface', help=help, default='localhost')

    options, args = parser.parse_args()

    return options


if __name__ == "__main__":
    options = parse_args()
    tracker = p2pchat.tracker.Tracker(options.iface, options.port)
    tracker.start()
