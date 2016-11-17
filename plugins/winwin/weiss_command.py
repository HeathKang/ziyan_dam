# -*- coding: utf-8 -*-

"""


"""

from __future__ import absolute_import

import sys

import time


from logbook import Logger

log = Logger('weiss_cmd')

from ziyan.lib.command_base import CommandBase

class WeissCommand(CommandBase):
    """ WEISS Command """
    
    def __init__(self, channel):
        """ 
        channel 
        
        """
        
        self.channel = channel
        
        super(WeissCommand, self).__init__()
        
    def run(self):        
        """ run and get values """

        while True:
            
            try:
                
                ### put msg to msg_queue
                cmd = {'cmd':'read'}
                self.put(cmd)
                log.debug(cmd)

            except Exception as ex:
                log.error(ex)
                
            time.sleep(self.conf[self.channel].get('interval', 10)) 
        #log.debug('run')