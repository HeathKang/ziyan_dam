# -*- coding: utf-8 -*-

"""
WinWin Worker

"""

from __future__ import absolute_import

import os
import sys

# find the plugins


import time
import traceback

import msgpack
from redis.exceptions import ConnectionError,NoScriptError

from logbook import Logger

log = Logger('worker')

from maboio.lib.redis_lib import RedisClient
from maboio.lib.influxdb_lib import InfluxC

from lib.winwin_lib import WinWin

class Worker(object):
    """ worker find content in windows """
    
    def __init__(self, conf):
        """ init """
        
        self.conf = conf
        
        self.winwin = WinWin(conf['station'])
        
        self.influxc = InfluxC(conf['influxdb'])    

        self.red = RedisClient(conf['redis'])
        
        self.interval = conf['app']['interval']
        self.title_like = conf['app']['title_like']        
        
        self.tags = conf['output']['tags']
        self.measurement = conf['output']['measurement']             
        self.red.load_script(conf['output']['enqueue_script'])
        
        ### find window
        self.winwin.get_win_list(self.title_like)
        
        self.fields = {}
        
        self.text_pos = {}
        
    def build_json(self):
        """ build json for influxdb """
        
        data = [{"time":int(time.time()), "measurement":self.measurement, \
                "tags":self.tags, "fields":self.fields}]
        
        return data        
        
    def build_fields(self):
        """ build fields for influxdb json  """
        #log.debug("build_fields")
        for hwnd in self.winwin.win_list:
                            
            self.winwin.get_child_list(hwnd)
            
            for parent_hwnd in self.winwin.win_dict:
                
                #log.debug(hex(hwnd_parent))
                #log.debug("##" * 20)
                for item in self.winwin.win_dict[parent_hwnd]:
                    #log.debug("****"*20)
                    #log.debug("%s-[%s]-%s-%s" %(item[0], hex(item[1]), item[2], item[3]))
                    #log.debug("****"*20)
                    
                    class_name, child_hwnd, parent_title, title = item
                    
                    #log.debug("%s,%s" %(hex(child_hwnd), class_name))
                    
                    (left, top, right, bottom) = self.winwin.get_rect(child_hwnd)
                    #log.debug("%s,%s,%s,%s" %(left, top, right, bottom))
                    #log.debug("class name:%s" % class_name)
                    
                    
                    title = self.winwin.get_title(child_hwnd)
                    #log.debug("[%s][%s] parent title:%s" % (hex(child_hwnd), title, parent_title))
                    if class_name == 'Edit':
                        

                        
                        text = self.winwin.get_value(child_hwnd)
                        #log.debug("text:%s" % text)
                        if text != '':
                            self.fields['edit1'] = text
                    # Current Sequence Statistics
                    elif class_name == 'SysListView32' or class_name == 'ListBox':
                        data = self.winwin.get_list_view_items(parent_hwnd, column_index= 1)
                        log.debug(hex(parent_hwnd))
                        
                        #v = self.winwin.get_parent_info(parent_hwnd)
                        #log.debug("%s - %s" %(hex(v[0]), v[1]))
                        #v = self.winwin.get_parent_info(v[0])
                        #log.debug("%s - %s" %(hex(v[0]), v[1]))
                        #if v[1] == 'Channel Counters':
                        #    self.fields['counter1'] = int(data[0])
                        #    self.fields['counter2'] = int(data[1])
                        log.debug(data)
                    
                    elif class_name == 'ThunderRT6TextBox' and parent_title == 'Current Sequence Statistics':                      
                        title = self.winwin.get_value(child_hwnd) #self.winwin.get_title(child_hwnd)
                        log.debug("###############[%s]" % (title))
                        log.debug("###>%s [%s,%s,%s,%s][%s]" % (title, left, top, right, bottom, left+top+right+bottom))

                        self.fields['total_time'] = title                    
                    elif class_name == 'ThunderRT6TextBox' and parent_title == 'Current Status':                      
                        title = self.winwin.get_title(child_hwnd)
                        log.debug("===>%s [%s,%s,%s,%s][%s]" % (title, left, top, right, bottom, left+top+right+bottom))

                        self.fields['sequence'] = title
                        
                    elif class_name == 'ProgressBar20WndClass' and parent_title == 'Current Status':
                        pos, range = self.winwin.get_progress(child_hwnd)
                        self.fields['progress'] = pos/range
                        log.debug("%s:%s" % (pos, range))
                            
    def enqueue(self):
        """ put data to queue in redis """
        
        if len(self.fields) >0 :
            json_data = self.build_json()
            log.debug(json_data)
            
            ### send data to influxdb
            #influxc.send(json_data)
            eqpt_no = "abc"
            timestamp = int(time.time())
            cmd = "cmd"
            measurement = "RPC"
            rawdata = self.fields
            data = self.fields
            
            log.debug(self.fields)
            
            rtn = self.red.enqueue(eqpt_no, timestamp, cmd, msgpack.packb(rawdata),
                                 msgpack.packb(data), 
                                 measurement.lower())
            log.debug(rtn)
            
        elif len( self.winwin.win_dict) > 0:
            pass
        else:
            log.debug("find window again...")
            self.winwin.get_win_list(self.title_like)
                    
    def run(self):
        """ run the job """
        
        
        
        while True:
            
            ### init fields each round
            self.fields = {}
            
            try:
                #log.debug("abc")
                self.build_fields()
                log.debug(self.fields)
                self.enqueue()
                
            except ConnectionError as err:

                log.error(traceback.format_exc())

            except NoScriptError as err:
                
                log.error(traceback.format_exc())
                try:
                    self.red.load_script(self.conf['output']['enqueue_script'])
                except:
                    pass

            except AttributeError as err:
                log.error(traceback.format_exc())

            except Exception as ex:
                log.error(traceback.format_exc())            
                log.debug("find window again...")
                self.winwin.get_win_list(self.title_like)
                
            time.sleep(self.interval)