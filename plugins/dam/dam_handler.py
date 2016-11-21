# -*- coding: utf-8 -*-

"""
dam_data handler

"""

from __future__ import absolute_import

import msgback

from logbook import Logger

log = Logger('dam_handler')

from maboio.lib.redis_lib import RedisClient

from ziyan.lib.handler_base import HandlerBase


class DamHandler(HandlerBase):
    """ msg processor for Dam"""
    
    def __init__ (self,channel):
        """
        channel 
        
        """
        self.channel = channel
        
        super(DamHandler,self).__init__()
        
        log.debug('---' * 25 )
        
        log.debug('---' * 25)
        
        
        if self.conf['logging']['debug']:
            
            log.debug('no redis connected')
            
        else:
            self.red = RedisClient(self.conf['redis'])
            self.red.load_script(self.conf['output']['enqueue_script'])
            
    def process(self,**kwargs):
        """
        process 
        
        """
        rtn = self.red.enqueue(eqpt_no = kwargs['eqpt_no'],
                        timestamp = kwargs['timestamp'],
                        cmd =   kwargs['cmd'],
                        rawdata = msgback.packb(kwargs['rawdata']),
                        data = msgback.packb(kwargs['data']),
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
                
                if fields == 'stop it':
                    log.warning("stop by msg")
                    break
                    
                log.debug(self.conf[self.channel])

            log.debug(fields)

            eqpt_no = self.conf['dam_equipment']['equipmentno']

            timestamp = fields['timestamp']

            # log.debug(button_status)
            for i in fields['payload']:

                measurement = 'DAM_TEM_Value'
                for line in fields['payload'][i]:
                    data = line
                    rawdata = line
                    log.debug(data)
                    # msg = {'uuid':uid, 'timestamp':timestamp,'type':type, 'channel':self.channel, 'interval':interval, 'payload ':payload}
                    self.process(eqpt_no=eqpt_no,
                                 timestamp=timestamp,
                                 cmd='STR',
                                 rawdata=rawdata,
                                 data=data,
                                 measurement=measurement)
                    # msg_queue.task_done()


        except Exception as ex:
        log.error(ex)


                
                
            
            
            
            
            
            
            
            
            
            
            