#!/usr/bin/env python3

import argparse
import p2pchat.trackerclient
import p2pchat.p2pConnection
import p2pchat.uiInterface
import p2pchat.dbConnection
from twisted.internet import reactor


def parse_args():
    description = """
This is the client for the p2p kademlia chat protocol
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
    # TODO: get p2p bootstrapaddresses
    p2p = p2pchat.p2pConnection.p2pConnection(args.host)
    dbConn = p2pchat.dbConnection.dbConnection()

    p2pchat.uiInterface.UIInterface(p2p, trackerclient, dbConn)

    reactor.run()


if __name__ == "__main__":
    main()
