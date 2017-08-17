#!/usr/bin/env python3

import p2pchat.tracker

if __name__ == "__main__":
    bindaddr = ('127.0.0.1', 1337)
    tracker = p2pchat.tracker.Tracker(bindaddr)
    tracker.start()
    tracker.stop()
