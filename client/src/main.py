#!/usr/bin/env python3

import p2pchat.trackerclient

if __name__ == "__main__":
    trackerclient = p2pchat.trackerclient.TrackerClient(('localhost', 1337)) 
    trackerclient.connect()
    trackerclient.disconnect()

