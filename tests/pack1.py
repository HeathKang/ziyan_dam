

import struct



STX = 0x02
ETX = 0x03
BLANK = 0x20
K = ord('K')

cmd = 'ASTZ'

clen = len(cmd)
channel_number = ord(str(0))
# AK Command telegram
fmt = "!2b%ds5b" % (clen)

buf = struct.pack(fmt, STX, BLANK, cmd, BLANK, K, channel_number, BLANK, ETX)

print buf

