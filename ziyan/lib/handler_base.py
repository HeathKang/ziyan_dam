
from __future__ import absolute_import

from sys import version_info

if version_info[0] == 3:
    from ziyan.lib.sharedq3 import SharedQ
else:
    from ziyan.lib.sharedq2 import SharedQ

class HandlerBase(object):
    """ handle base """
    
    def __init__(self):
        
        ### singleton Q 
        self.g = SharedQ()
        
        ### singleton conf 
        self.conf = self.g.conf
        
    def get(self):
        return self.g.msg_queue.get()        