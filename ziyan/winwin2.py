# -*- coding: utf-8 -*-

"""
WinWin main

"""

from __future__ import absolute_import

import os
import sys

import traceback

import time

# find the plugins
sys.path.append(os.getcwd())

from win32con import BM_GETSTATE, BM_GETIMAGE
#from commctrl import 

from pywinauto import findwindows
from pywinauto.controls.win32_controls import ListBoxWrapper, ButtonWrapper
from pywinauto.controls.common_controls import ListViewWrapper, _listview_item
from pywinauto.controls.common_controls import TreeViewWrapper

from logbook import Logger

log = Logger('main')


from maboio.lib.setup_logger import setup_logger
from maboio.lib.opts import get_option_parser
from maboio.lib.utils import get_conf

#from lib.worker import Worker

def work(conf):
    
    windows = findwindows.find_windows(title_re = "Chamber")
    log.debug(windows)
    #log.debug(hex(windows[0]))
    
    
    log.debug("##"*20)
    
    hwnd = 0x00010266
    
    listbox = ListBoxWrapper(hwnd)
    
    ct = listbox.ItemCount()
    
    log.debug(ct)
    
    for text in listbox.ItemTexts():
        log.debug(text)
    

        
def work2(conf):
    
    log.debug("##"*20)
    
    hwnd = 0x00010292
    
    
    listbox2 = ListBoxWrapper(hwnd)
    
    ct = listbox2.ItemCount()
    
    log.debug(ct)
    
    for text in listbox2.ItemTexts():
        log.debug(text)
    
        
    """
    hwnd = 0x00010BA8
    
    treeview = TreeViewWrapper(hwnd)
    
    ct = treeview.ItemCount()
    
    log.debug(ct)
    
    hwnd = 0x00010666
    
    listview = ListViewWrapper(hwnd)
    
    cc = listview.ItemCount()
    
    log.debug(cc)
    
    
    items = listview.Items()
    
    li = _listview_item(listview, 12)
    
    log.debug(listview.Texts())
    
    for item in items:
        #log.debug(item)
        pass
        
        
    """
    
    
def work3(conf):
    """
    ['CaptureAsImage', 'Check', 'CheckByClick', 'CheckByClickInput', 'Children', 'Class', 'Click', 'ClickInput', 'ClientRect', 'ClientRects', 'ClientToScreen', 'Close', 'CloseAltF4', 'CloseClick', 'ContextHelpID', 'ControlCount', 'ControlID', 'DebugMessage', 'DoubleClick', 'DoubleClickInput', 'DragMouse', 'DragMouseInput', 'DrawOutline', 'ExStyle', 'Font', 'Fonts', 'FriendlyClassName', 'GetActive', 'GetCheckState', 'GetFocus', 'GetProperties', 'GetShowState', 'GetToolbar', 'HasExStyle', 'HasStyle', 'IsActive', 'IsChild', 'IsDialog', 'IsEnabled', 'IsUnicode', 'IsVisible', 'Maximize', 'Menu', 'MenuItem', 'MenuItems', 'MenuSelect', 'Minimize', 'MoveMouse', 'MoveMouseInput', 'MoveWindow', 'NotifyParent', 'Owner', 'Parent', 'PopupWindow', 'PostCommand', 'PostMessage', 'PressMouse', 'PressMouseInput', 'ProcessID', 'Rectangle', 'ReleaseMouse', 'ReleaseMouseInput', 'Restore', 'RightClick', 'RightClickInput', 'Scroll', 'SendCommand', 'SendMessage', 'SendMessageTimeout', 'SetApplicationData', 'SetCheckIndeterminate', 'SetFocus', 'SetTransparency', 'SetWindowText', 'Style', 'Texts', 'TopLevelParent', 'TypeKeys', 'UnCheck', 'UncheckByClick', 'UncheckByClickInput', 'UserData', 'VerifyActionable', 'VerifyEnabled', 'VerifyVisible', 'WheelMouseInput', 'WindowText', '_NeedsImageProp', '__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_as_parameter_', '_cache', '_menu_handle', '_scroll_types', 'actions', 'appdata', 'can_be_label', 'friendlyclassname', 'handle', 'has_title', 'ref', 'windowclasses', 'writable_props']
    """
    
    hwnd = 0x00250234
    btn = ButtonWrapper(hwnd)
    #log.debug(dir(btn))

    log.debug(btn.SendMessage(BM_GETSTATE))
    #log.debug(btn.SendMessage(BM_GETIMAGE))
    #fn = "%s.png" % int(time.time())
    
    #btn.CaptureAsImage(fn)
    log.debug(btn.Style())
    log.debug(btn.NotifyParent("1"))
    log.debug(btn.ref)
    #log.debug(btn.GetProperties().keys())
    
    
    d = btn.GetProperties()
    img = d['Image']
    
    #btn.SetWindowText("BTN")
    
    fn = "%s.jpg" %(int(time.time()))
    
    #img.save(fn)
    for item in d :
        try:
            #print(item) ,
            #print "--", 
            pass
            #print(d[item])
        except:
            #log.debug(traceback.format_exc())
            log.debug("======== %s =========" % item)
    
    
    
    
    
def main():
    """ main """
    
    appname = "winwin"
    
    parser = get_option_parser(appname)    
    options, args = parser.parse_args()    

    conf_file = os.path.abspath(options.config)    
    
    conf = get_conf(conf_file)
    
    setup_logger(conf['logging'])
    
    log.debug("start...")
    
    while True:
    
        #work(conf)
        work(conf)
        work2(conf)
        time.sleep(2)
    #worker = Worker(conf)
    
    #worker.run()


if __name__ == "__main__":
    main()
