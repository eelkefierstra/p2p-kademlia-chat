#!/usr/bin/env python3

import os.path
import argparse
from p2pchat.trackerclient import TrackerClient
from p2pchat.p2p_connection import P2PConnection
from p2pchat.application import Application
from p2pchat.db_connection import DBConnection


def parse_args():
    description = """
This is the client for the p2p kademlia chat protocol
"""

    parser = argparse.ArgumentParser(description=description)

    help_port = "The port to connect to. Default to 1337."
    parser.add_argument('--port', type=int, help=help_port, default=1337)

    # Dynamic port range: 49152-65535
    help_port_p2p = ("The port to listen on for P2P connections."
                     " Default to 8468.")
    parser.add_argument('--port-p2p', type=int, help=help_port_p2p,
                        default=8468)

    help_host = "The host to connect to."
    parser.add_argument('--host', help=help_host, default='192.168.80.130')

    help_localdb = "The local database location."
    # TODO create script which will create this directory and add chown -R
    # vagrant:vagrant

    user_home = os.path.expanduser('~')
    db_loc = os.path.join(user_home, '.p2pchat', 'p2pchat.db')
    app_data_dir = os.path.dirname(os.path.abspath(db_loc))
    if not os.path.isdir(app_data_dir):
        os.makedirs(app_data_dir)
    parser.add_argument('--localdb', help=help_localdb,
                        default=db_loc)


    args = parser.parse_args()
    print(args)

    return args


def main():
    args = parse_args()

    p2p = P2PConnection(args.port_p2p)

    db_conn = DBConnection(args.localdb)

    def setup_db_failed(failure):
        print("Setting up the db failed: {}".format(failure.getErrorMessage()))
        from twisted.internet import reactor
        reactor.stop()
    d = db_conn.setup_db()
    d.addErrback(setup_db_failed)

    app = Application(p2p, db_conn)

    trackerclient = TrackerClient(args.host, args.port, notifier=app)

    app.set_trackerclient(trackerclient)


    from twisted.internet import reactor
    reactor.callWhenRunning(app.start, args.host)
    reactor.run()


if __name__ == "__main__":
    main()
