# -*- coding: gb2312 -*-

"""
WinWin

- pywin32

"""

from __future__ import absolute_import

import struct
import codecs
import traceback

from logbook import Logger

log = Logger('winwin')

import ctypes

import win32api, win32gui
import win32con

from win32con import PAGE_READWRITE, MEM_COMMIT, MEM_RESERVE, MEM_RELEASE,\
    PROCESS_ALL_ACCESS
    
import commctrl
from commctrl import LVM_GETITEMTEXT, LVM_GETITEMCOUNT,\
    LVM_GETHEADER

GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
OpenProcess = ctypes.windll.kernel32.OpenProcess
WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
ReadProcessMemory = ctypes.windll.kernel32.ReadProcessMemory
memcpy = ctypes.cdll.msvcrt.memcpy


class WinWin(object):
    
    def __init__(self, conf):
        """  """
        
        self.conf = conf
        
        self.class_name_list = self.conf["class_name_list"]
        
        self.parent_title_list = None
        
        #self.title = title
        

        #app window list
        self.win_list = []
        
        #child window list
        self.win_dict = {}
        
        self.target_list = []
        
    def get_title(self, hwnd):
        return win32gui.GetWindowText(hwnd)
        
    def get_rect(self, hwnd):
        
        return win32gui.GetWindowRect(hwnd)

    def callback(self, hwnd, title_like):
        """ find top window  """
        
        title = win32gui.GetWindowText(hwnd)
        try:
            #log.debug(type(title))
            #log.debug(type(title_like))
            #if title.count( title_like.encode('utf8') ) ==1:
            title = codecs.decode(title,('gb2312'),'strict')
            title_like = codecs.decode(title_like,('utf8'),'strict')
            #log.debug(repr(title))
            #log.debug(repr(title_like))
            #log.debug(type(title))
            if title.count(title_like) == 1:
                log.debug("##" * 20)
                log.debug(hex(hwnd))                
            #if title.count(title_like) ==  1:
                #print("in callback")
                #print("hwnd:", hex(hwnd), title)
                #win = hwnd
                self.win_list.append(hwnd)
        except Exception as ex:
            #print(hwnd)
            log.error(traceback.format_exc())
            
    def get_win_list(self, title_like):
        """ find top window by callback """
        #self.init()
        self.win_list = []
        self.win_dict = {}
        win32gui.EnumWindows(self.callback, title_like)
        
        
    def get_parent_info(self, hwnd):
        
            parent_hwnd = win32gui.GetParent(hwnd)
            #log.debug("parent hwnd: %s" % parent_hwnd)
            
            ### get parent title
            parent_title = win32gui.GetWindowText(parent_hwnd)    
            
            return (parent_hwnd, parent_title)
       
    
    def callback_child(self, hwnd, wildcard):
        """ find child window """
        
        #log.debug("hwnd:%s" % hwnd)
        

            
        try:
        
            ### get title
            title = win32gui.GetWindowText(hwnd)
            #log.debug("title:%s" % title)
            
            ### get parent hwnd
            parent_hwnd = win32gui.GetParent(hwnd)
            #log.debug("parent hwnd: %s" % parent_hwnd)
            
            ### get parent title
            parent_title = win32gui.GetWindowText(parent_hwnd)
            #log.debug("parent tilte: %s" % parent_title)
            
            ### get class name
            class_name = win32gui.GetClassName(hwnd)
            
            
            if class_name in self.class_name_list:
                
                
                if hwnd in self.win_dict:
                    pass
                else:
                    self.win_dict[hwnd] = []                
                
                
                #log.debug("title:%s" % title)
                #log.debug("class name: %s" % class_name)
                #log.debug("parent tilte: %s" % parent_title)
                
                if (class_name, hwnd) in self.win_dict[hwnd]:
                    pass
                else:
                
                    if self.parent_title_list == None:
                        self.win_dict[hwnd].append((class_name, hwnd, parent_title, title))
                    
                    elif parent_title in self.parent_title_list:
                            
                            #self.target_list.append((class_name, hwnd))
                            
                            self.win_dict[hwnd].append((class_name, hwnd, parent_title, title))
                    else:
                        #log.debug((title, parent_hwnd, parent_title, class_name))#print(hwnd, title, cls)
                        pass
        except Exception as ex:
            log.error(ex)
            
    def get_child_list(self, hwnd):
        """ find child window list by callback_child """
        
        ### EnumChildWindows
        #self.init()
        self.win_dict = {}
        win32gui.EnumChildWindows(hwnd, self.callback_child, "*") 
        
    def get_value(self, hwnd):
        """ get Text field value """
        
        buf_size = 1 + win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)

        #print(buf_size)

        if buf_size:
            buffer = win32gui.PyMakeBuffer(buf_size)
            win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, buffer)
            txt = buffer[:buf_size-1] 
            
            ### codecs.decode() - API 2.7
            ### codecs.decode() - API 3.5
            val = codecs.decode(txt, 'utf-8', 'strict') 
            #print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " Value:", val)
            #print(type(txt))
            return val
            #return txt

    def get_value3(self, hwnd):
        
        buf_size = 1 + win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)

        #print("buf_size ", buf_size)

        if buf_size:
            buffer = win32gui.PyMakeBuffer(buf_size)
            win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, buffer)
            txt = buffer[:buf_size-1]            
            return txt
            #val = codecs.decode(txt, encoding='utf-16', errors='strict') 
            #print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), " Value:", val)
            
    def get_list_view_items(self, hwnd, column_index=0):

        # Allocate virtual memory inside target process
        pid = ctypes.create_string_buffer(4)
        p_pid = ctypes.addressof(pid)
        GetWindowThreadProcessId(hwnd, p_pid) # process owning the given hwnd
        hProcHnd = OpenProcess(PROCESS_ALL_ACCESS, False, struct.unpack("i",pid)[0])
        pLVI = VirtualAllocEx(hProcHnd, 0, 4096, MEM_RESERVE|MEM_COMMIT, PAGE_READWRITE)
        pBuffer = VirtualAllocEx(hProcHnd, 0, 4096, MEM_RESERVE|MEM_COMMIT, PAGE_READWRITE)

        # Prepare an LVITEM record and write it to target process memory
        lvitem_str = struct.pack('iiiiiiiii', *[0,0,column_index,0,0,pBuffer,4096,0,0])
        lvitem_buffer = ctypes.create_string_buffer(lvitem_str)
        copied = ctypes.create_string_buffer(4)
        p_copied = ctypes.addressof(copied)
        WriteProcessMemory(hProcHnd, pLVI, ctypes.addressof(lvitem_buffer), ctypes.sizeof(lvitem_buffer), p_copied)

        # iterate items in the SysListView32 control
        num_items = win32gui.SendMessage(hwnd, LVM_GETITEMCOUNT)
        item_texts = []
        for item_index in range(num_items):
            win32gui.SendMessage(hwnd, LVM_GETITEMTEXT, item_index, pLVI)
            target_buff = ctypes.create_string_buffer(4096)
            ReadProcessMemory(hProcHnd, pBuffer, ctypes.addressof(target_buff), 4096, p_copied)
            item_texts.append(target_buff.value)

        VirtualFreeEx(hProcHnd, pBuffer, 0, MEM_RELEASE)
        VirtualFreeEx(hProcHnd, pLVI, 0, MEM_RELEASE)
        win32api.CloseHandle(hProcHnd)
        return item_texts            
            
    def get_list_view_items_X(self, hwnd, column_index=0):
        """  get values from SysListView32 / ListView """
        
        # Allocate virtual memory inside target process
        pid = ctypes.create_string_buffer(4)
        p_pid = ctypes.addressof(pid)
        GetWindowThreadProcessId(hwnd, p_pid) # process owning the given hwnd
        print pid
        #print """---"""
        hProcHnd = OpenProcess(PROCESS_ALL_ACCESS, False, struct.unpack("i",pid)[0])
        print hex(hProcHnd)
        pLVI = VirtualAllocEx(hProcHnd, 0, 4096, MEM_RESERVE|MEM_COMMIT, PAGE_READWRITE)
        pBuffer = VirtualAllocEx(hProcHnd, 0, 4096, MEM_RESERVE|MEM_COMMIT, PAGE_READWRITE)

        # Prepare an LVITEM record and write it to target process memory
        lvitem_str = struct.pack('iiiiiiiii', *[0,0,column_index,0,0,pBuffer,4096,0,0])
        lvitem_buffer = ctypes.create_string_buffer(lvitem_str)
        copied = ctypes.create_string_buffer(4)
        p_copied = ctypes.addressof(copied)
        WriteProcessMemory(hProcHnd, pLVI, ctypes.addressof(lvitem_buffer), ctypes.sizeof(lvitem_buffer), p_copied)

        # iterate items in the SysListView32 control
        num_items = win32gui.SendMessage(hwnd, commctrl.LVM_GETITEMCOUNT)
        print "num_items", num_items
        print win32gui.GetClassName(hwnd)
        item_texts = []
        for item_index in range(num_items):
            x = win32gui.SendMessage(hwnd, 12, 0, pLVI)
            print "x", x,pLVI,win32con.WM_GETTEXT
            target_buff = ctypes.create_string_buffer(4096)
            print target_buff.value
            ReadProcessMemory(hProcHnd, pBuffer, ctypes.addressof(target_buff), 4096, p_copied)
            item_texts.append(target_buff.value)

        VirtualFreeEx(hProcHnd, pBuffer, 0, MEM_RELEASE)
        VirtualFreeEx(hProcHnd, pLVI, 0, MEM_RELEASE)
        win32api.CloseHandle(hProcHnd)
        #print item_texts
        return item_texts
        
    def get_tree_view_items(self):
        """  TreeView """
        
        pass
        
    def get_progress(self, hwnd):
        """ 
        get progress bar info
        GETPOS & GETRANGE 
        """
        
        pos = win32gui.SendMessage(hwnd, commctrl.PBM_GETPOS,0,0)
        range = win32gui.SendMessage(hwnd, commctrl.PBM_GETRANGE,0,0)
        
        if range == 0:
            range = 1
            raise(Exception("range is zero"))
        
        #print("%.2f %%" %(100.0*pos/range))
        
        return (pos, range)  