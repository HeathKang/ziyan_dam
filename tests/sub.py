#!/usr/bin/env python
# coding:utf8
#author: wangqiankun@lashou-inc.com

import zmq
import time,sys


def main():

    if len(sys.argv) < 2:
        print "Usage: subscriber [topic topic]"
        #sys.exit(1)

    connect_to = 'tcp://127.0.0.1:5000'# sys.argv[1]
    topics = ['sports.general','sports.football'] #sys.argv[2:]

    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect(connect_to)

    #manage subscriptions

    if not topics:
        print "Receiving messages on ALL topics...."
        s.setsockopt(zmq.SUBSCRIBE,'')
    else:
        print "Receiving messages on topics: %s..." %topics

        for t in topics:
            s.setsockopt(zmq.SUBSCRIBE,t)

            print
    try:
        while True:
            topics,msg = s.recv_multipart()
            print 'Topic:%s,msg:%s' %(topics,msg)
    except KeyboardInterrupt:
        pass
    print "Done...."


if __name__ == "__main__":
    main()