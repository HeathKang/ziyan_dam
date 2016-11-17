# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import time
import struct
import socket

import threading

import binascii

from logbook import Logger

log = Logger('ak_lib')

STX = 0x02
ETX = 0x03
BLANK = 0x20
K = ord('K')


AK_CONNECTED     = 1
AK_DISCONNECTED  = 0


class AKClient(object):
    """ AK Client """

    def __init__(self, conf):
        """ init """
        
        self.conf = conf
        
        log.debug(conf)
        
        self.host = conf["host"]
        self.port = conf["port"]
        
        self.channel_number = conf["channel_number"]
        
        self.timeout = conf["timeout"]
        self.allowed_cmds = set()
        
        for item in conf["allowed_cmds"]:
            
            self.allowed_cmds.add(item.upper())
        
        log.debug(self.allowed_cmds)
        
        self.status = AK_DISCONNECTED
        self.error_msg = None
        
        self.lock = threading.Lock() 

    def connect(self):
        """ connect """
        
        if not self.lock.locked():
            self.lock.acquire()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
            self.sock.settimeout(self.timeout)
        
            try:
                log.debug("connect {}:{}".format(self.host, self.port))
                self.sock.connect((self.host, self.port))
                self.status = AK_CONNECTED
            except:
                self.status = AK_DISCONNECTED
                #raise Exception("no connection")
            finally:
                self.lock.release()
        else:
            self.status = AK_DISCONNECTED
            log.warning("locked")

    def __del__(self):
        """   """
        
        #log.debug("__del__")
        
        if self.status == AK_CONNECTED:
            log.debug("socket close")
            self.sock.close()

    def _send(self, buf):
        """ send """
        
        if self.status == AK_CONNECTED:
            try:
                self.sock.sendall(buf)
                return AK_CONNECTED
            except Exception as ex:
                #log.debug(ex)
                self.error_msg = ex.message
                self.connect()
                return self.status
                #return AK_DISCONNECTED
                #raise(Exception(ex))
        else:
            return AK_DISCONNECTED

    def _recv(self):
        """ recv """

        try:
            data = self.sock.recv(1024)
            
        except Exception as ex:
            log.debug(ex)
            self.error_msg = ex.message
            #raise(Exception(ex))
            self.connect()
        else:
            return data
        
    def validate(self, cmd):
        """   """
        
        if cmd in self.allowed_cmds:
            return True
        else:
            return False
            
    def query_aflt(self, code):
        
        cmd = 'AFLT'
        
        #channel_number = 1
        
        msg = self.pack(cmd, self.channel_number, code)

        status = self._send(msg)
        
        if status == AK_CONNECTED:

            data_recv = self._recv()
            
            #print(data_recv)
            
            fmt = '2b4s2b%dsb' % (len(data_recv)-9)
            
            out = struct.unpack(fmt, data_recv)
        
        #print out
        
        #out = self.unpack(data_recv) 

        #print cmd, code, out[5]
        
            
    def query(self, cmd, code=None):
        """ query """
        
        # channel number for build struct
        cmd = cmd.upper() 
        
        log.debug(cmd)
        
        #channel_number = 0
        result = {}        
        data = {}        
        #cmds_set = set()        
        #for cmd in cmds:            
        cmd = cmd.upper()        
        if self.validate(cmd):
            #cmds_set.add(cmd)
            #pass

            #continue
                
            #log.debug(cmds_set)
            
          
            
            #for cmd in cmds_set:
                
            msg = self.pack(cmd, self.channel_number, code)

            status = self._send(msg)

            if status == AK_CONNECTED:
                
                data_recv = self._recv()
                
                #print(data_recv)
                
                
                #fmt = ""
                #print struct.unpack(fmt, data_recv)
                
                
                out = self.unpack(cmd, data_recv)
                #print(len(out))

                
                if len(out) > 6:
                    data[cmd] = out[6]
                else:
                    data[cmd] = cmd
              
                return data
            else:
                log.warning("no connection")
                self.connect()
                return {"error":"no connection"}

        else:
            msg = "not allowed:[%s]" % (cmd)
            log.warning(msg)
            return {"error":msg}

            
    def query_all(self, cmds):
        """ query """
        
        # channel number for build struct
        #channel_number = 0

        result = {}
        
        data = {}
        
        cmds_set = set()
        
        for cmd in cmds:
            
            cmd = cmd.upper()
            
            if self.validate(cmd):
                cmds_set.add(cmd)
            else:
                log.warning("not allowed:[%s]" % (cmd))
                continue
                
        log.debug(cmds_set)
        
      
        
        for cmd in cmds_set:
            
            msg = self.pack(cmd, self.channel_number)

            self._send(msg)

            data_recv = self._recv()
            #print(data_recv)
            out = self.unpack(data_recv)
            #print(len(out))

            
            if len(out) > 6:
                data[cmd] = out[6]
            else:
                data[cmd] = cmd
      
        return data


    def pack(self, cmd, channel_number, code = None):
        """ AK command pack """

        #cmd = "AVFI"
        #print(channel_number, cmd, code)
        #cmd = cmd.upper()
        
        
        if cmd =='AFLT':
            """ The dyno will return the fault text within double quotes (102 characters max data.)
                If the fault number is not found, just the two double quotes will be returned.
            """
            
            if code == None:
                raise(Exception("The fault number must be specified with the AFLT request."))
                
            else:
                
                clen = len(cmd)
                
                xlen = len(code)

                # AK Command telegram
                fmt = "!2b%dsb%ds5b" % (clen, xlen)
                #print fmt
                #channel_number = 0

                buf = struct.pack(fmt, STX, BLANK, cmd, BLANK, code, BLANK, K, channel_number, BLANK, ETX)
                #log.debug(buf)
                return buf            
                    
        else:
          
            
            clen = len(cmd)

            # AK Command telegram
            fmt = "!2b%ds5b" % (clen)
            #print fmt
            #channel_number = 0

            buf = struct.pack(fmt, STX, BLANK, cmd, BLANK, K, channel_number, BLANK, ETX)
            #log.debug(buf)
            return buf

    def unpack(self, cmd, data):
        """ AK unpack """

        if data == None:
            raise(Exception("data is None"))
            
        dlen = len(data) - 10
        
        if cmd == 'AFLT':
            fmt = '2b4s2b%dsb' % (len(data)-9)

        elif dlen < 0:
            #raise Exception("struct error")
            fmt = "!2b4s3b"

        else:
            # AK Response telegram
            fmt = "!2b4s3b%ds1b" % (dlen)

        try:
            val = struct.unpack(fmt, data)
            
            #print(type(val))
            # tuple
            log.debug(val)
            return val
        except Exception as ex:
            #log.error(ex.message)
            b64 = binascii.b2a_base64(data)
            log.error(b64)
            return {"error":ex.message,"base64":b64}
            #raise Exception("unpack exception")