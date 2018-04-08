#!/usr/bin/env python3

import os
import argparse
from p2pchat.p2p_connection import P2PConnection
from p2pchat.tracker import Tracker
from p2pchat.database import P2PChatDB


def check_file_exists(parser, filepath):
    if not os.path.exists(filepath):
        parser.error("The file {} does not exist!".format(filepath))
    return filepath


def parse_args():
    description = """
This is the tracker server for the p2p kademlia chat protocol.

"""

    parser = argparse.ArgumentParser(description=description)
    helpPort = "The port to listen on. Defaults to 1337."
    parser.add_argument('--port', type=int, help=helpPort, default=1337)

    helpIface = "The interface to listen on. Default is localhost."
    parser.add_argument('--bindaddr', help=helpIface, default='localhost')

    helpDbHost = "The database host. Default is localhost."
    parser.add_argument('--dbhost', help=helpDbHost, default='localhost')

    helpDbPort = "The database port. Default is 27017."
    parser.add_argument('--dbport', type=int, help=helpDbPort, default=27017)

    helpDbPrivkey = "The private key file"
    parser.add_argument('dbprivkey', type=lambda x: check_file_exists(parser, x), help=helpDbPrivkey)

    helpDbCert = "The certificate file"
    parser.add_argument('dbcert', type=lambda x: check_file_exists(parser, x), help=helpDbCert)

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()

    p2pServer = P2PConnection()
    db = P2PChatDB(args.dbhost, args.dbport, args.dbprivkey, args.dbcert)
    db.connect()
    tracker = Tracker(args.bindaddr, args.port, db)

    from twisted.internet import reactor
    tracker.start(reactor)
    reactor.run()
