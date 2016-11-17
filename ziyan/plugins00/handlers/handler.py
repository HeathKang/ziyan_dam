# -*- coding: utf-8 -*-

"""
msg handler

"""

from __future__ import absolute_import

from sys import version_info

import msgpack

from logbook import Logger

log = Logger('handler')

from maboio.lib.redis_lib import RedisClient

if version_info[0] == 3:
    from winwin.lib.sharedq3 import SharedQ
else:
    from winwin.lib.sharedq2 import SharedQ

     
class MsgHandler(object):
    """ msg processor for winwin """
    
    def __init__(self):
        """ init """
        
        #self.conf = conf
        
        self.g = SharedQ()
        
        ### singleton conf        
        self.conf = self.g.conf
        
        if self.conf['logging']['debug']:
            #print "%%%" * 20
            log.debug('no redis connected')
            pass
        else:
            self.red = RedisClient(self.conf['redis'])        
            self.red.load_script(self.conf['output']['enqueue_script'])

    def process(self):
        """ process msg """
        
        rtn = self.red.enqueue(eqpt_no = eqpt_no, timestamp = timestamp, cmd = cmd, 
                            rawdata = msgpack.packb(rawdata),
                            data = msgpack.packb(data), 
                            measurement = measurement.lower())
        log.debug(rtn)
        
    def run(self):
        """ loop """
        
        while True:
            
            try:                
                #log.debug("queue size: %d" % self.g.msg_queue.qsize())
                line = self.g.msg_queue.get()
                
                if line == 'stop it':
                    log.warning("stopped by msg")
                    break
                
                log.debug(line)
                
                #msg_queue.task_done()
                
            except Exception as ex:
                log.error(ex)
                