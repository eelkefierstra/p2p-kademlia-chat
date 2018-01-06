#!/usr/bin/env python3

import argparse
import os
from p2pchat.tracker import Tracker
from p2pchat.database import P2PChatDB

def check_file_exists(parser, filepath):
    if not os.path.exists(filepath):
        parser.error("The file {} does not exist!".format(arg))
    return filepath

def parse_args():
    description = """
This is the tracker server for the p2p kademlia chat protocol.

"""

    parser = argparse.ArgumentParser(description=description)

    help = "The port to listen on. Default to a random available port."
    parser.add_argument('--port', type=int, help=help, default=1337)

    help = "The interface to listen on. Default is localhost."
    parser.add_argument('--iface', help=help, default='localhost')

    help = "The database host. Default is localhost."
    parser.add_argument('--dbhost', help=help, default='localhost')

    help = "The database port. Default is 27017."
    parser.add_argument('--dbport', type=int, help=help, default=27017)

    help = "The private key file"
    parser.add_argument('dbprivkey', type=lambda x:check_file_exists(parser, x), help=help)

    help = "The certificate file"
    parser.add_argument('dbcert', type=lambda x: check_file_exists(parser, x), help=help)

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    db = P2PChatDB(args.dbhost, args.dbport, args.dbprivkey, args.dbcert)
    db.connect()
    tracker = Tracker(args.iface, args.port, db)
    tracker.start()
