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

    def run(self):
        """ thread """

        while True:

            try:

                log.debug(self.g.queues.keys())

                cmd = self.get_cmd()

                log.debug(cmd)

                # cmd = 'ASTZ'
                rawdata = self.mod.query(cmd['cmd'])
                data = self.inject_payload(int,rawdata)

                log.debug(data)

                self.put(data)



                                # time.sleep(3)
            except Exception as ex:

                log.error(ex)