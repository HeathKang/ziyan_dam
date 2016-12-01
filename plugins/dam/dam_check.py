# -*- coding: utf-8 -*-

"""
plugin for Modbus Client

"""
from __future__ import absolute_import

import os
import sys

import uuid

import time

from logbook import Logger

log = Logger('ak_chk')

from maboio.lib.utils import fn_timer

# from lib.sharedq import SharedQ
from ziyan.lib.exceptions import NoDataException

from ziyan.lib.mod_lib  import ModbusClient
from ziyan.lib.check_base import CheckBase


class DAMCheck(CheckBase):
    def __init__(self, plugin):

        # log.debug(__file__)
        #


        super(DAMCheck, self).__init__(__file__, plugin)

        # self.conf = conf
        log.debug(self.conf)
        log.debug(">>>" * 20)
        self.mod = ModbusClient(self.conf['equipment'])

        self.connect()

    def connect(self):
        """ connect ak host """

        self.mod.connect()

    def readdata(self,cmd):
        """ read data from modbus"""

        data = {}

        for unit in self.conf['equipment']['units']:

            rawdata = self.mod.query(cmd,self.conf['equipment']['addr'],self.conf['equipment']['count'],unit)

            data.update({ unit : rawdata })
        return data

    def format(self,data,conf):
        """ get data from different register address and format"""

        if 'STR_B' in conf:
            for unit in data:
                data_a = data[unit][:4]
                data_b = data [unit][13:16]
                data_c = data[unit][7:9]

                data[unit] = data_a + data_b + data_c

            return data

        else:
            return data

    def parse(self,data):
        """ handle data """

        for unit in data:
            L = []
            tem_data = data[unit][:4]
            tem_data_handle = [ (100*(1.2 * 20 * float(d)/0xfff - 4)/16.0) for d in tem_data ]

            pd_data = data[unit][4:6]
            pd_data_handle = []

            for d in pd_data:
                I = float(1.2 * 20 * int(d) / 0xfff)

                dt = int(round((I - 4) * 2))
                pd_data_handle.append(dt)

            hdtmp_data = data[unit][5]


            hdsatu_data = data[unit][6]


            L = L + tem_data_handle + pd_data_handle
            print (L)
            L = L + [hdtmp_data] + [hdsatu_data]


            data[unit] = L

        return data

    def data_payload(self,payload):
        """

            inject payload into msg body
            msg_data = [
                    {'uuid': uid, 'timestamp': timestamp,
                   'unit': unit, 'payload ': payload[unit]},
                    {'uuid': uid, 'timestamp': timestamp,
                   'unit': unit, 'payload ': payload[unit]}
                    ...
            ]

        """
        msg_data = []
        for unit in payload:

            uid = str(uuid.uuid4())

            timestamp = time.time()

            msg = {'uuid': uid, 'timestamp': timestamp,
                   'unit': unit, 'payload': payload[unit]}

            msg_data.append(msg)

        return msg_data


    def run(self):
        """ thread """

        while True:



            log.debug(self.g.queues.keys())

            cmd = self.get_cmd()

            log.debug(cmd)

            # cmd = 'ASTZ'
            readdata = self.readdata(cmd['cmd'])



            data = self.format(readdata,cmd['cmd'])
            data = {1:[1,2,3,4,5,6,7]}

            data = self.parse(data)

            data = self.data_payload(data)

            log.debug(data)

            self.put(data)



                                # time.sleep(3)


