# -*- coding: utf-8 -*-

"""


"""

from __future__ import absolute_import

import sys
import time

from logbook import Logger

log = Logger('dam_cmd')

from ziyan.lib.command_base import CommandBase


class DAMCommand(CommandBase):
    """ AK Command for BEP """

    def __init__(self, plugin):
        """
        channel

        """

        # self.channel = channel

        super(DAMCommand, self).__init__(__file__, plugin)

        self.cmds = self.conf['cmds']

        self.interval = self.conf['interval']

    def run(self):
        """ run and get values """

        while True:

            try:

                ### put msg to msg_queue
                # cmds = ['ASTZ', 'ASTF']


                log.debug(self.cmds)

                for item in self.cmds:
                    cmd = {'cmd': item}
                    self.put(cmd)
                    log.debug(cmd)

            except Exception as ex:
                log.error(ex)

            time.sleep(self.interval)

            # time.sleep(self.conf[self.channel].get('interval', 10))
            # log.debug('run')
