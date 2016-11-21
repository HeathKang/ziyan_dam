
from __future__ import absolute_import

from sys import version_info

from ziyan.lib.base import Base

if version_info[0] == 3:
    from ziyan.lib.sharedq3 import SharedQ
else:
    from ziyan.lib.sharedq2 import SharedQ

class HandlerBase(Base):
    """ handle base """
    
    def __init__(self,path_plugin,plugin_conf):
        
        ### singleton Q
        super(HandlerBase,self).__init__(path_plugin,plugin_conf)

    def put(self,cmd):

        self.out_q.put(cmd)
        
    def get(self):

        return self.in_q.get()