# -*- coding: utf-8 -*-
"""
maboio
"""

from __future__ import absolute_import

from queue import Queue
    
from maboio.common.singleton import Singleton

#QUEUE_BUFFER_SIZE = 200
#msg_queue= Queue(QUEUE_BUFFER_SIZE)

class SharedQ(metaclass=Singleton):
    """ shared object """
    
    #__metaclass__ = Singleton

    def __init__(self, conf=None):
        """ init """
        
        self.conf = conf
        buffer_size = conf['app'].get('buffer_size', 100)
        #self.cmd_queue = Queue(QUEUE_BUFFER_SIZE)
        self.cmd_queue= Queue(buffer_size)
        self.msg_queue= Queue(buffer_size)