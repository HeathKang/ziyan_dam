# -*- coding: utf-8 -*-

"""
plugin for WEISS Chamber screen reader

"""
from __future__ import absolute_import

import sys

import time

import win32gui
import commctrl

from pywinauto import findwindows
from pywinauto import handleprops

from pywinauto.controls.win32_controls import ListBoxWrapper, ButtonWrapper
from pywinauto.controls.common_controls import ListViewWrapper, _listview_item
from pywinauto.controls.common_controls import TreeViewWrapper

from logbook import Logger

log = Logger('weiss_check')

from maboio.lib.utils import fn_timer

#from lib.sharedq import SharedQ
from ziyan.lib.exceptions import NoDataException

from ziyan.lib.check_base import CheckBase

#for module in sys.modules:
#    log.debug(module)
#    pass
#print "##"*20

class WeissCheck(CheckBase):
    """ WEISS Checker """
    def __init__(self, channel):
        """ 
        channel 
        
        """
        
        self.channel = channel
        
        super(WeissCheck, self).__init__()
        #CheckBase.__init__(self)
        self.windows = []
        self.child_windows = []        
    
    def init(self):
        """ find target window and controls once """
        
        log.debug('init...')
        
        self.check_proc()
        
        self.find_targets()
        
        #self.find_window()        
        #self.find_child_windows()
        
    def find_targets(self):
        """ find target window"""
        
        self.windows = findwindows.find_windows(title_re = "Settings")
        
        if len(self.windows) == 0:
            log.debug('no window found')
        else:
            log.debug(self.windows)
            hwnd = self.windows[0]
            
            self.child_windows = handleprops.children(hwnd)

    def find_child_windows(self):
        """ find child windows """
        
        if self.window:
            self.child_windows = handleprops.children(self.window)
        else:
            raise(Exception('no window found'))

    @fn_timer
    def get_values(self):
        """ values from windows """
        
        #windows = findwindows.find_windows(parent = self.window)#, class_name = 'Edit')        
        
        win_ctrl = {}
        
        values = []
        
        for hwnd in self.child_windows:
            
            parent = handleprops.parent(hwnd)
            
            parent_text = handleprops.text(parent)
            
            ### picked tab
            if parent_text in [ 'Serial Bridge', 'Proxy']:        

                if parent_text not in win_ctrl:
                    win_ctrl[parent_text] = {}
                
                classname = handleprops.classname(hwnd)
                
                if classname in ['Edit']:
                    
                    text = handleprops.text(hwnd)
                    rect = handleprops.rectangle(hwnd)
                    
                    #log.debug("%s,%s,%s - %s" % (parent, classname, text, parent_text))
                    #log.debug("(%s,%s)" % (rect.top, rect.left))
                    #val = (rect.top, rect.left)
                    win_ctrl[parent_text][(rect.top, rect.left)] = text                    
        
        if len(win_ctrl) == 0:
            raise(NoDataException('no data found'))
            
        for key in win_ctrl:
            log.info(key)            
            data = win_ctrl[key]
            log.info(data)
            
            ### sort by (top, left) #(y,x)
            vals = sorted(data.items(),key=lambda item: item[0])
            #log.debug(vals)
            fields = {}
            
            for i, item in enumerate(vals, 1):
                #line = "%s:%s" % (i, item[1])
                #log.debug(line)
                fields[i] = item[1]
            
            log.debug(self.conf[self.channel])
            
            """
            sensu-monitoring-platform
            
            event:            
            - action
            - occurrences [redis]            
            - client
                -- name
                -- address
                -- timestamp            
            - check
                -- name
                -- issued
                -- subscirbers []
                -- handler
                -- history []
                -- interval
                -- output
                -- command
                -- status

            """
            ### msg
            
            values.append(fields)
            
               
            
            #log.debug('=='*20)         
        return values
        #log.debug(win_ctrl)

        #log.debug(windows)
        
    def get_listbox_values(self, hwnd):
        """ listbox """
        
        listbox = ListBoxWrapper(hwnd)
        
        ct = listbox.ItemCount()
        
        log.debug(ct)
        
        for text in listbox.ItemTexts():
            log.debug(text)
            
    def get_listview_values(self, hwnd):
        """ syslistview32 """
        
        listview = ListViewWrapper(hwnd)
        
        ct = listview.ItemCount()
        
        log.debug(ct)
        
        i = 1
        
        li = _listview_item(listview, i)
        
        log.debug(listview.Texts())        
        
        for text in listview.ItemTexts():
            log.debug(text)
        pass
        
    def get_treeview_values(self, hwnd):
        """ systreeview32 """
        
        treeview = TreeViewWrapper(hwnd)
        
        ct = treeview.ItemCount()
        
        log.debug(ct)
        
        for text in treeview.ItemTexts():
            log.debug(text)
        
    def get_progress(self, hwnd):
        """ progress bar for MTS RPC """
        
        pos = win32gui.SendMessage(hwnd, commctrl.PBM_GETPOS,0,0)
        range = win32gui.SendMessage(hwnd, commctrl.PBM_GETRANGE,0,0)
        
        if range == 0:
            range = 1
            raise(Exception("range is zero"))
        
        #print("%.2f %%" %(100.0*pos/range))
        
        return (pos, range)        
        
    def get_text_value(self, hwnd):
        """ get text from Edit """
        
        return handleprops.text(hwnd)
        
    def get_button_status(self, hwnd):
        """ img button for WEISS """
        
        btn = ButtonWrapper(hwnd)
        #log.debug(dir(btn))

        #log.debug(btn.SendMessage(BM_GETSTATE))
        #log.debug(btn.SendMessage(BM_GETIMAGE))
        
        #fn = "%s.png" % int(time.time())
        
        img = btn.CaptureAsImage()
        
        conf = {'p1':(39, 42), 'p2':(36, 46), 'p3':(20,11), "green":(0, 255, 0), "white":(255, 255, 255), "p":(198, 198, 198)}
        
        self.conf.update(conf)
        
        left = 1
        top = 1
        
        ### check visiable
        if left > 0 and top > 0:            
            pass
        
        ### green
        rgb1 = im.getpixel(self.p1)
        
        ### white
        rgb2 = im.getpixel(self.p2)
        
        ###
        rgb3 = im.getpixel(self.p3)
        
        #assert rgb1 == self.conf['green']
        if rgb1 == self.conf['green']  and rgb3 == self.conf['p']:
            ### running
            return True

        if rgb2 == self.conf['white'] and rgb3 == self.conf['p']:
            ### stoped
            return False        
        
    def get_multi_text_values(self):
        """ multi texts in one frame """
        
        pass
        
    def process(self):
        """ data process """
        
        pass
        
    def run(self):        
        """ run and get values """
        
        ### find target once
        self.init()

        while True:
            
            try:
                
                cmd = self.get_cmd()
                
                log.debug(cmd)
                
                values = self.get_values()
                
                for payload in values:
                    
                    msg = self.inject_payload(type='data', payload = payload)
            
                    ### put msg to msg_queue
                    self.put(msg) 
            
            except NoDataException as ex:
                log.error(ex)
                ### find target again
                self.init()
            except Exception as ex:
                log.error(ex)
                
                ### find target again
                #self.init()
            else:
                self.process()
            # log.debug('---' * 20)
            #time.sleep(self.conf[self.channel].get('interval', 10)) 
        #log.debug('run')