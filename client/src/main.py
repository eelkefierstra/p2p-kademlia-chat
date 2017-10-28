#!/usr/bin/env python3

import p2pchat.trackerclient
import p2pchat.p2pConnection

def main():
    p2p = p2pchat.p2pConnection.p2pConnection(['127.0.0.1',50040]) #TODO: get bootstrapaddresses
    p2p.send('Test message to test p2p network.')
    print p2p.get('Test')

    trackerclient = p2pchat.trackerclient.TrackerClient(('localhost', 1337))
    trackerclient.connect()
    trackerclient.disconnect()

if __name__ == "__main__":
    main()
