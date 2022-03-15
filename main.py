import xbee
import time
import struct

# Config
# Console Logging (3 Verbose, 2 Info, 1 Warning, 0 Error, -1 Off)
intLogLevel = 2

# Endpoint Definition
listEndpoints = {
    b'\x01': { # TODO: Auto increment addresses, or statically define them?
        'type': b'\x02\x00',
        'clustersRX': [
            b'\x00\x00',
            b'\x03\x00',
            b'\x06\x00'
        ],
        'clustersTX': [
            # None
        ]
    }
}

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

# Hang out until we're connect, then get our 16-bit Network Address
while xbee.atcmd('AI') > 0:
    ''' TODO: Report status nicely (not just the raw value)
    0   - Success
    33  - Scan found no PANs
    34  - Scan found no valid PANs based on SC and ID settings
    35  - Valid PAN found, but joining is currently disabled
    36  - No joinable beacons were found
    255 - Initializing; no status has been determined yet
    '''
    log(3, 'Network not ready: %s' % (xbee.atcmd('AI')))
    time.sleep_ms(500)
strNA16 = struct.pack('<i', xbee.atcmd('MY'), 'little')[:2]
log(2, 'Our 16-bit Network Address is: %s' % (hex(xbee.atcmd('MY'))[2:]))
