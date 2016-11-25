# -*- coding: utf-8 -*-

"""
plugin for Modbus Client

"""
from __future__ import absolute_import

import os
import sys

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

    def parse(self,data):
        """ handle data """

        L=[]
        tem_data = data [:4]
        tem_data_handle = [ (100*(1.2 * 20 * float(d)/0xfff - 4)/16.0) for d in tem_data ]

        pd_data = data[4]
        pd_data_handle = int(round((float(1.2 * 20 * int(pd_data)/0xfff) - 4)/2))

        hdtmp_data = data[5]
        hdtmp_data_handle = 125 * (1.2 * 16 * float(hdtmp_data)/0xfff) - 25

        hdsatu_data = data [6]
        hdsatu_data_handle = 100 * (1.2 * 16 * float(hdsatu_data)/0xfff)

        L = (L + tem_data_handle).append(pd_data_handle)
        L = L.append(hdtmp_data_handle)
        L = L.append(hdsatu_data_handle)

        return L


    def run(self):
        """ thread """

        while True:

            try:

                log.debug(self.g.queues.keys())

                cmd = self.get_cmd()

                log.debug(cmd)

                # cmd = 'ASTZ'
                rawdata = self.mod.query(cmd['cmd'])

                data = self.parse(rawdata)

                data = self.inject_payload(int,data)

                log.debug(data)

                self.put(data)



                                # time.sleep(3)
            except Exception as ex:

                log.error(ex)