# -*- coding: utf-8 -*-
"""
maboio
"""

from __future__ import absolute_import

from Queue import Queue
    
from maboio.common.singleton import Singleton

#QUEUE_BUFFER_SIZE = 200
#msg_queue= Queue(QUEUE_BUFFER_SIZE)

class Global(object):
    """ shared object """
    
    __metaclass__ = Singleton

    def __init__(self, conf=None):
        """ init """
        
        self.conf = conf
        
        self.buffer_size = conf['app'].get('buffer_size', 100)
        #self.cmd_queue = Queue(QUEUE_BUFFER_SIZE)
        
        self.queues = {}
        
    def get_queue(self, queue_name):
        """ get queue from dict """
        
        if queue_name == '':
            return None
            
        if queue_name in self.queues:
            return self.queues[queue_name]            
        else:
            self.queues[queue_name] = Queue(self.buffer_size)
            return self.queues[queue_name]
            
            
        #self.cmd_queue= Queue(self.buffer_size)
        #self.msg_queue= Queue(self.buffer_size)
