# -*- coding: utf-8 -*-

"""
WinWin main

- WEISS
- MTS Station
- MTS RPC
- MTS MTP
- ..

"""
from __future__ import absolute_import

__author__ = "mabo.io"
__copyright__ = "mabo.io"
__license__ = "MIT"
__version__ = "0.2.4"

import os
import sys
# find the plugins
sys.path.append(os.getcwd())

from logbook import Logger
log = Logger('main')

from sys import version_info

import time
import traceback
import threading

#import chardet

### maboio lib
from maboio.lib.setup_logger import setup_logger
from maboio.lib.opts import get_option_parser
from maboio.lib.utils import get_conf, get_class

### lib
#from lib.exceptions import NoDataException

### hidden import
if version_info[0] == 3:
    from ziyan.lib.global3 import Global
else:
    from ziyan.lib.global2 import Global

import msgpack
import maboio.lib.redis_lib

from ziyan.lib.exceptions import NoDataException
#from ziyan.lib.checker_base import CheckerBase

### plugins
#from plugins.checkers.checker import Checker
#from plugins.handlers.handler import MsgHandler

def setup(conf):
    """ init threads
    
    - checker
    - handler
    
    [checker] --results--> [handler] ----> [filter](redis) ---->     
    
    """
    
    log.info("init...")    
    
    #_, SharedQ = get_class("winwin.lib.sharedq.SharedQ")
    
    ### init shared Queue and configuration (singleton)
    g = Global(conf)
    
    plugins = conf['app']['plugin']#['plugins']#['plugins.checkers.checker.Checker', 'plugins.handlers.handler.MsgHandler']
    
    thread_set = set()
    
    thread_name_set = set()
    
    for plugin in plugins:
        
        plugins_name = plugin['path']
        channel = plugin['channel']
        
        log.debug(plugins_name)
        
        ### load plugin Klass dynamically
        class_name, Klass = get_class(plugins_name)
        log.debug(conf)
        #log.debug(conf[channel])
        log.debug("===" * 20)
        worker = Klass(plugin)
        
        thread_name = "t_%s" %(channel)
        
        if thread_name in thread_name_set:
            raise Exception("thread name exists")
        else:
            thread_name_set.add(thread_name)
        
        t_worker = threading.Thread(target = worker.run, name=thread_name, args=[])
        t_worker.setDaemon(True)
        t_worker.start()
        
        thread_set.add(thread_name)
        
    t_watchdog = threading.Thread(target = watchdog, name='watchdog', args=[thread_set])
    t_watchdog.setDaemon(True)
    t_watchdog.start()    
    
    #return thread_set

    """
    commander = Commander(conf['input'])
    
    t_commander = threading.Thread(target = commander.run, name="commander", args=[])
    t_commander.setDaemon(True)
    t_commander.start()
    """
    
def watchdog(plugin_threads):
    """ 
    watchdog threads
    
    """
    
    while True:
        
        threads = set()
        
        for item in threading.enumerate():
            threads.add( item.name )

        log.debug("###"*20)
        log.debug(plugin_threads)
        log.debug(threads)
        
        ### check if the worker thread is there.
        if not threads.issuperset(plugin_threads):
            ### stop thread and start again
            #setup(conf)
            pass
            
        time.sleep(10)#conf['app']['interval'])
        
def main(appname):
    """ main """   
    
    ### prepare configuration and logger
    
    parser = get_option_parser(appname)    
    options, args = parser.parse_args()    

    conf_file = os.path.abspath(options.config)    
    
    conf = get_conf(conf_file)
    
    setup_logger(conf['logging'])
    
    log.debug("start...")
    
    ### init threads
    setup(conf)    

    ### main loop
    while True:
        
        time.sleep(1)    

if __name__ == "__main__":
    
    appname = "ziyan"
    
    main(appname)
