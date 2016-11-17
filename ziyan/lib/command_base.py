# -*- coding: utf-8 -*-

from __future__ import absolute_import

from sys import version_info

import time
import uuid

import psutil

from logbook import Logger
log = Logger('checker')

from maboio.lib.utils import fn_timer

from ziyan.lib.base import Base



class CommandBase(Base):
    """ checker base class, worker for gather information from screen """
    
    def __init__(self, path_plugin, plugin):
        """ init """        
        #self.conf = conf
        #self.g = Global()
        super(CommandBase, self).__init__(path_plugin, plugin)
        ### get configuration
        #self.g_conf = self.g.conf
        
        #self.conf = self.g.conf[channel]
        
        #self.in_q = self.g.get_queue(self.conf['in_q'])
        #self.out_q = self.g.get_queue(self.conf['out_q'])
        
    def put(self, cmd):
        """ put msg into msg_queue """
        
        self.out_q.put(cmd)
        
    def get(self):
        """ put msg into msg_queue """
        
        return self.in_q.get()        

    def run(self):        
        """ run and get values """

        while True:
            
            try:
                
                ### put msg to msg_queue
                cmd = {'cmd':'base read'}
                self.put(cmd)
                log.debug(cmd)

            except Exception as ex:
                log.error(ex)
                
            time.sleep(self.conf[self.channel].get('interval', 10)) 