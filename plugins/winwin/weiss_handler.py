# -*- coding: utf-8 -*-

"""
msg handler

"""

from __future__ import absolute_import

#from sys import version_info

import msgpack

from logbook import Logger

log = Logger('weiss_handler')

from maboio.lib.redis_lib import RedisClient

from ziyan.lib.handler_base import HandlerBase
     
     
class MsgHandler(HandlerBase):
    """ msg processor for winwin """
    
    def __init__(self, channel):
        """ 
        channel 
        
        """
        self.channel = channel
        #self.conf = conf
        
        super(MsgHandler, self).__init__()
        
               
        #self.conf = self.g.conf
        
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
                ### get msg from msg_queue
                line = self.get()
                
                if line == 'stop it':
                    log.warning("stopped by msg")
                    break
                
                log.debug(self.conf[self.channel])
                
                log.debug(line)
                
                #msg_queue.task_done()
                
            except Exception as ex:
                log.error(ex)
                