# -*- coding: utf-8 -*-

lines2 = """
T.Chamber       癈     21.836    -90.000    190.000
T.air outlet    癈     21.730    -90.000    190.000
T.WSF           癈     21.970    -90.000    190.000
T.Outer Air     癈     23.500    -90.000    190.000
P.Diff.-pres.   Pa      10.220   -400.000    400.000
T.Suction_CM1   癈      2.869    -90.000    190.000
T.Suction_CM2   癈     14.880    -90.000    190.000
T.Suction_CM3   癈     26.048    -90.000    190.000
T.Hotgas_CM1    癈     84.470    -90.000    190.000
T.Hotgas_CM2    癈     38.050    -90.000    190.000"""

import chardet

v = b'癈'

print(repr(lines2))

print chr(0x88)

print chardet.detect(bytearray([0xe7, 0x99, 0x88]))

print v#.decode('windows-1252')

x = b'°'

print repr(x)

print chardet.detect(x)