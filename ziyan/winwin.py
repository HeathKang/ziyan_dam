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
__version__ = "0.2.3"

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
from lib.sharedq import SharedQ

### hidden import
from lib.exceptions import NoDataException
from lib.checker_base import CheckerBase

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
    
    g = SharedQ(conf)
    
    plugins = conf['app']['plugins']#['plugins']#['plugins.checkers.checker.Checker', 'plugins.handlers.handler.MsgHandler']
    
    thread_set = set()
    
    for plugins_name in plugins:
        
        #plugins_name = plugin['path']
        log.debug(plugins_name)
        
        ### load plugin Klass dynamically
        class_name, Klass = get_class(plugins_name)
        
        worker = Klass()
        
        t_worker = threading.Thread(target = worker.run, name=class_name, args=[])
        t_worker.setDaemon(True)
        t_worker.start()
        
        thread_set.add(class_name)
    
    return thread_set

    """
    commander = Commander(conf['input'])
    
    t_commander = threading.Thread(target = commander.run, name="commander", args=[])
    t_commander.setDaemon(True)
    t_commander.start()
    """
    
def main():
    """ main """    
    
    appname = "winwin"
    
    ### prepare configuration and logger
    
    parser = get_option_parser(appname)    
    options, args = parser.parse_args()    

    conf_file = os.path.abspath(options.config)    
    
    conf = get_conf(conf_file)
    
    
    
    setup_logger(conf['logging'])
    
    log.debug("start...")
    
    ### init threads
    plugin_threads = setup(conf)
    
    ### main loop
    while True:
        
        threads = set()
        
        for item in threading.enumerate():
            #print dir(item)
            #print item
            if item.name == 'Checker':
                #item.exits()
                pass
            threads.add( item.name )

        #log.debug(plugin_threads)
        #log.debug(threads)
        ### check if the worker thread is there.
        if not threads.issuperset(plugin_threads):
            ### stop thread and start again
            #setup(conf)
            pass
        time.sleep(conf['app']['interval'])
        
def test():
    
    t = (0, 255, 0)
    l = [0, 255, 0]
    assert tuple(l) == t
    assert list(t) == l

if __name__ == "__main__":
    
    main()
