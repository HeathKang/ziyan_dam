# -*- coding: utf-8 -*-

from __future__ import absolute_import
"""
import os
from sys import version_info



from maboio.lib.utils import get_conf

if version_info[0] == 3:
    from ziyan.lib.sharedq3 import SharedQ
else:
    from ziyan.lib.global2 import Global
"""
import time
import uuid

import psutil

from logbook import Logger
log = Logger('checker')

from maboio.lib.utils import fn_timer
from ziyan.lib.base import Base

class CheckBase(Base):
    """ checker base class, worker for gather information from screen """
    
    def __init__(self, path_plugin, plugin):
        """ init """        
        #self.conf = conf
        """
        self.g = Global()
        
        ### get configuration
        #self.conf = self.g.conf
        #self.conf = self.g.conf[channel]
        
        dir_plugin = os.path.dirname(path_plugin)
        conf_file_name = "{}.toml".format(channel)
        conf_file = os.sep.join([dir_plugin, conf_file_name])
        
        self.conf = get_conf(conf_file)['plugin']
        
        
        self.in_q = self.g.get_queue(self.conf['in_q'])
        self.out_q = self.g.get_queue(self.conf['out_q'])
        """
        super(CheckBase, self).__init__(path_plugin, plugin)
        
        #self.channel = plugin['channel']
        
    def inject_payload(self, type, payload):
        """ inject payload into msg body """
        
        uid = str(uuid.uuid4())
        
        timestamp = time.time()
        
        interval = self.conf.get('interval',0)
        
        msg = {'uuid':uid, 'timestamp':timestamp,'type':type, 
                'channel':self.channel, 'interval':interval, 'payload ':payload}
        
        return msg
        
    def put(self, msg):
        """ put msg into msg_queue """
        
        self.out_q.put(msg)

    def get_cmd(self):
        """ put msg into msg_queue """
        
        cmd = self.in_q.get()
        
        return cmd

    @fn_timer
    def check_proc(self):
        """ psutil to check process """
        
        log.debug('check proc')
        
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name','create_time'])
            except psutil.NoSuchProcess:
                pass
            else:
                if pinfo['name'] == 'python.exe':
                    print(pinfo) 