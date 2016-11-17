# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
from sys import version_info

#import time
#import uuid

#import psutil

from logbook import Logger
log = Logger('base')

#from maboio.lib.utils import fn_timer

from maboio.lib.utils import get_conf

if version_info[0] == 3:
    from ziyan.lib.global3 import Global
else:
    from ziyan.lib.global2 import Global
    
class Base(object):
    
    def __init__(self, path_plugin, plugin):
        
        self.g = Global()
        
        ### get configuration
        #self.conf = self.g.conf
        #self.conf = self.g.conf[channel]
        
        self.channel = plugin['channel']
        
        dir_plugin = os.path.dirname(path_plugin)
        
        conf_file_name = "{}.toml".format(self.channel)
        
        conf_file = os.sep.join([dir_plugin, conf_file_name])
        
        self.conf = get_conf(conf_file)['channel']
        
        
        self.in_q = self.g.get_queue(plugin['in_q'])
        self.out_q = self.g.get_queue(plugin['out_q'])     