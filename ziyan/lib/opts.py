
from __future__ import absolute_import

import os
import optparse


def get_option_parser(name):

    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`airgparse.Namespace`
    """

    conf = "conf/%s.toml" %(name)
    
    parser = optparse.OptionParser(name)
        
    parser = optparse.OptionParser(
        'Usage: %prog [options] path.to.maboio')

    parser.add_option('-c', '--conf', dest='config',
                      help='config file', action='store', type='string', default=conf)                                            

    parser.add_option('-l', '--logfile', dest='logfile',
                      help='write logs to FILE', metavar='FILE')
    parser.add_option('-v', '--verbose', dest='verbose',
                      help='verbose logging', action='store_true')                      
    parser.add_option('-q', '--quiet', dest='verbose',
                      help='log exceptions only', action='store_false')
    parser.add_option('-w', '--workers', dest='workers', type='int',
                      help='worker threads (default=1)', default=3)      
        
    return parser