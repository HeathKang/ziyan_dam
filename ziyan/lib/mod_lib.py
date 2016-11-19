# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging
import time
import struct
import socket

import threading

import binascii

from logbook import Logger
from pymodbus.client.sync import  ModbusSerialClient

log = Logger('mod_lib')

MOD_CONNECTED = 1
MOD_DISCONNECTED = 0


class ModbusClient(object):
    """ AK Client """

    def __init__(self, conf):
        """ init """

        self.conf = conf

        log.debug(conf)

        self.protocol =conf['protocol']
        self.port = conf["port"] # pc port COM
       # self.addr = hex(conf["addr"]) # the start of registers
        self.addr = int(conf["addr"],base=16)
        print("addr++" * 60)
        log.debug(self.addr)
        print("addr++" * 60)
        
        self.baudrate = conf["baudrate"]

        self.count = conf["count"] # the number of register
        #self.unit = hex(conf["unit"]) #the unit of registers
        self.unit =  int(conf["unit"],base=16)
        print("unit++" * 60)
        log.debug(self.unit)
        print("unit++" * 60)

        self.timeout = conf["timeout"]
        self.allowed_cmds = set()

        for item in conf["allowed_cmds"]:
            self.allowed_cmds.add(item.upper())

        log.debug(self.allowed_cmds)

        self.status = MOD_DISCONNECTED
        self.error_msg = None

        self.lock = threading.Lock()

    def connect(self):
        """ connect """

        if not self.lock.locked():
            self.lock.acquire()
            self.client =  ModbusSerialClient(self.protocol, port=self.port,baudrate=self.baudrate, timeout=self.timeout)


            try:
                log.debug("connect {}".format(self.port))
                self.status = MOD_CONNECTED
            except:
                self.status = MOD_DISCONNECTED
                # raise Exception("no connection")
            finally:
                self.lock.release()
        else:
            self.status = MOD_DISCONNECTED
            log.warning("locked")

    def __del__(self):
        """   """

        # log.debug("__del__")

        if self.status == MOD_CONNECTED:
            log.debug("connent close")
            self.client.close()

    def _recv(self):
        """ recv """

        try:
            data = self.client.read_holding_registers(self.addr, count=self.count, unit=self.unit)

        except Exception as ex:
            log.debug(ex)
            self.error_msg = ex.message
            # raise(Exception(ex))
            self.connect()
        else:
            return data.registers

    def validate(self, cmd):
        """   """

        if cmd in self.allowed_cmds:
            return True
        else:
            return False

    def parse(self,data):
        '''parse the recive data '''

        data = [(100 * (1.2 * 20 * float(d) / 0xfff - 4) / 16.0) for d in data]

        return data



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



            if self.status == MOD_CONNECTED:

                data_recv = self._recv()

                #print(data_recv)


                #fmt = ""
                #print struct.unpack(fmt, data_recv)
                data = self.parse(data_recv)


                #print(len(out))

                return data

            else:
                log.warning("no connection")
                self.connect()
                return {"error":"no connection"}

        else:
            msg = "not allowed:[%s]" % (cmd)
            log.warning(msg)
            return {"error":msg}

