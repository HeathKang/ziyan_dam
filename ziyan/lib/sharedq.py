# -*- coding: utf-8 -*-
"""
maboio
"""

from __future__ import absolute_import

from sys import version_info

if version_info[0] == 2:
    from Queue import Queue
else:
    from queue import Queue
    
from maboio.common.singleton import Singleton

#QUEUE_BUFFER_SIZE = 200
#msg_queue= Queue(QUEUE_BUFFER_SIZE)

class SharedQ2(object):
    """ shared object """
    
    __metaclass__ = Singleton

    def __init__(self, conf=None):
        """ init """
        
        self.conf = conf
        buffer_size = conf['app'].get('buffer_size', 10)
        #self.cmd_queue = Queue(QUEUE_BUFFER_SIZE)
        self.msg_queue= Queue(buffer_size)


class SharedQ3(metaclass=Singleton):
    """ shared object """
    
    #__metaclass__ = Singleton

    def __init__(self, conf=None):
        """ init """
        
        self.conf = conf
        buffer_size = conf['app'].get('buffer_size', 10)
        #self.cmd_queue = Queue(QUEUE_BUFFER_SIZE)
        self.msg_queue= Queue(buffer_size)