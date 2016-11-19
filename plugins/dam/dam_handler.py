# -*- coding: utf-8 -*-

"""
plugin for BEP AK Client

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

from ziyan.lib.ak_lib import AKClient
from ziyan.lib.check_base import CheckBase


class BEPCheck(CheckBase):
    def __init__(self, plugin):

        # log.debug(__file__)
        #


        super(BEPCheck, self).__init__(__file__, plugin)

        # self.conf = conf
        log.debug(self.conf)
        log.debug(">>>" * 20)
        self.ak = AKClient(self.conf['equipment'])

        self.connect()

    def connect(self):
        """ connect ak host """

        self.ak.connect()

    def run(self):
        """ thread """

        while True:

            try:

                log.debug(self.g.queues.keys())

                cmd = self.get_cmd()

                log.debug(cmd)

                # cmd = 'ASTZ'
                rawdata = self.ak.query(cmd['cmd'])
                log.debug(rawdata)
                # time.sleep(3)

                cmd = 'ASTF'
                rawdata = self.ak.query(cmd)
                log.debug(rawdata)
                # time.sleep(0.3)
                if cmd == 'ASTF':
                    code_str = rawdata[cmd]
                    if code_str == 'ASTF':
                        pass
                    else:
                        code_list = code_str.split(',')
                        for code in code_list:
                            log.debug(code)
                            ### (2, 32, 'AFLT', 32, 50, '"Chamber is not ready !!! Can\'t operate dyno, check function of Chamber"', 3)
                            try:
                                error_msg = self.ak.query('AFLT', code)
                                log.debug(error_msg)
                            except Exception as ex:
                                log.debug(ex)

                                # time.sleep(3)
            except Exception as ex:

                log.error(ex)