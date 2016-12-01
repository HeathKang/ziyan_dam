# -*- coding: utf-8 -*-

"""
dam_data handler

"""

from __future__ import absolute_import

import msgpack
import time
from Queue import Queue #just for test

from logbook import Logger

log = Logger('dam_handler')

from maboio.lib.redis_lib import RedisClient

from ziyan.lib.handler_base import HandlerBase


class DAMHandler(HandlerBase):
    """ msg processor for Dam"""
    
    def __init__ (self,plugin):
        """
        channel 
        
        """
        
        super(DAMHandler,self).__init__(__file__,plugin)
        
        log.debug('---' * 25 )
        
        log.debug('---' * 25)


        self.red = RedisClient(self.conf['redis'])
        self.red.load_script(self.conf['output']['enqueue_script'])
            
    def process(self,**kwargs):
        """
        process 
        
        """
        rtn = self.red.enqueue(eqpt_no = kwargs['eqpt_no'],
                        timestamp = kwargs['timestamp'],
                        cmd =   kwargs['cmd'],
                        rawdata = msgpack.packb(kwargs['rawdata']),
                        data = msgpack.packb(kwargs['data']),
                        measurement = kwargs['measurement'])
        log.debug(rtn)
        
    def run(self):
        """
        loop
        
        """
        while True:

            try:
                ### get  msg from msg_queue

                fields = self.get()

                for field in fields:

                    timestamp = field['timestamp']
                    eqpt_no = field['unit']
                    print eqpt_no

                    # log.debug(button_status)
                    measurement = self.conf['dam_measurement']['measurement']
                    log.debug(fields)
                    # msg = {'uuid':uid, 'timestamp':timestamp,'type':type, 'channel':self.channel, 'interval':interval, 'payload ':payload}
                    self.process(eqpt_no=eqpt_no,
                                 timestamp=int(timestamp * (1000)),
                                 cmd='STR',
                                 rawdata=field['payload'],
                                 data=field['payload'],
                                 measurement=measurement)
                    # msg_queue.task_done()
                    print("*" * 50)
                    log.debug(int(timestamp))
                    print("*" * 50)
            except Exception as e:

                log.debug(e)




                
                
            
            
            
            
            
            
            
            
            
            
            