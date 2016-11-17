# -*- coding: utf-8 -*-

from __future__ import absolute_import

from logbook import Logger

log = Logger('main')

class DataBuilder(object):
    
    def __init__(self):
        pass
        
    def test(self):
        
        lines1 = u"""Temperature     °C     22.000   21.940  -55.000   45.000
rel. humidity   %rH      0.000   46.194    0.000  100.000
Humidity        g/kg    20.000    7.400  -10.000   35.000
Pressure        Pa      10.000   10.520 -400.000  400.000"""



        lines2 = u"""
T.Chamber       °C     21.836    -90.000    190.000
T.air outlet    °C     21.730    -90.000    190.000
T.WSF           °C     21.970    -90.000    190.000
T.Outer Air     °C     23.500    -90.000    190.000
P.Diff.-pres.   Pa     10.220   -400.000    400.000
T.Suction_CM1   °C      2.869    -90.000    190.000
T.Suction_CM2   °C     14.880    -90.000    190.000
T.Suction_CM3   °C     26.048    -90.000    190.000
T.Hotgas_CM1    °C     84.470    -90.000    190.000
T.Hotgas_CM2    °C     38.050    -90.000    190.000"""        
        
        
        for line in lines1.split('\n'):
            self.slice(line, '1')
        
        log.debug("=="*20)
        
        for line in lines2.split('\n'):
            
            self.slice(line, '2')
            
    def slice(self, line, listbox):
        """
        WEISS Chamber 
        - slice in lua?
        """
        
        if listbox == '1':
            # .strip()
            print [line[0:16], line[16:22], line[22:30], line[30:39], line[30:48], line[48:]]
        elif listbox == '2':
            print [line[0:16], line[16:20], line[20:29], line[29:40], line[40:]]

class Weiss_Chamber(object):
    """ object status"""
    
    def __init__(self):
        """ init """
