#!/usr/bin/env python
# coding:utf8
#author: wangqiankun@lashou-inc.com

import itertools
import sys,time
import zmq


def main():
    if len(sys.argv) != 2:
        print 'Usage: publisher'
        #sys.exit(1)
    bind_to = 'tcp://127.0.0.1:5000'# sys.argv[1]
    all_topics = ['sports.general','sports.football','sports.basketball','stocks.general','stocks.GOOG','stocks.AAPL','weather']

    ctx = zmq.Context()
    s = ctx.socket(zmq.PUB)
    s.bind(bind_to)

    print "Starting broadcast on topics:"
    print "%s" %all_topics
    print "Hit Ctrl-c to stop broadcasting."
    print "waiting so subscriber sockets can connect...."

    print
    time.sleep(1)
    msg_counter = itertools.count()

    try:
        for topic in itertools.cycle(all_topics):
            msg_body = str(msg_counter.next())
            #print msg_body,
            print 'Topic:%s,msg:%s' %(topic,msg_body)
            s.send_multipart([topic,msg_body])
            #s.send_pyobj([topic,msg_body])
            time.sleep(2)
    except KeyboardInterrupt:

        pass


    print "Wating for message queues to flush"

    time.sleep(0.5)
    s.close()
    print "Done"

if __name__ == "__main__":
    main()