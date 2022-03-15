import xbee
import time
import struct

# Config
# Console Logging (3 Verbose, 2 Info, 1 Warning, 0 Error, -1 Off)
intLogLevel = 2

def log(intLevel, strLog):
    if intLevel == 0: strLevel = 'ERR'
    elif intLevel == 1: strLevel = 'WRN'
    elif intLevel == 2: strLevel = 'IFO'
    elif intLevel == 3: strLevel = 'VBS'
    else: strLevel = '???'
    
    if intLevel <= intLogLevel:
        print("[%s] [%s] %s" % (int(time.ticks_ms()/1000), strLevel, strLog))
    return

# Get our 64-bit Network Address and convert to Little Endian
strNA64 = struct.pack('>i', int.from_bytes(xbee.atcmd('SL'), 'little')) + struct.pack('>i', int.from_bytes(xbee.atcmd('SH'), 'little'))
log(2, 'Our 64-bit Network Address is: %s' % (hex(int.from_bytes(struct.pack('>i', int.from_bytes(xbee.atcmd('SL'), 'little')) + struct.pack('>i', int.from_bytes(xbee.atcmd('SH'), 'little')), 'big'))[2:].upper()))
