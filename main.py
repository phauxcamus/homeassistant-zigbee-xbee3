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

def log(level: int, data: str):
    '''Simple wrapper for logging to UART.
 
    `level`: Verbose (3), Info (2), Warning (1), Error (0)
    `data`: Literal string of log data to output
    '''
    if level == 0: strLevel = 'ERR'
    elif level == 1: strLevel = 'WRN'
    elif level == 2: strLevel = 'IFO'
    elif level == 3: strLevel = 'VBS'
    else: strLevel = '???'
    
    if level <= intLogLevel:
        print("[%s] [%s] %s" % (int(time.ticks_ms()/1000), strLevel, data))
    return

def hwSleep(usec: int):
    '''Wrapper for forcing the XBee to sleep.
    
    `usec`: Sleep time in µs
    '''
    log(3, 'Sleeping for %sµs' % (usec))
    time.sleep_ms(usec) # TODO: Replace below with actual hardware sleep command
    return 

def setPWM(brightness: int, pwm1: bool = False):
    '''Set the PWM pin states by percentage
    
    `brightness`: Integer from 0 to 100
    `pwm1`: Set to True for PWM1, otherwise you're addressing PWM0
    '''
    try:
        xbee.atcmd('M'+int(pwm1), hex(int(brightness/100)*1023))
    except Exception as e:
        log(1, 'Failed to set PWM%s to %s%% (%s): %s' % (int(pwm1), brightness, hex(int(brightness/100)*1023).upper(), e))
        return False
    finally:
        log(2, 'PWM%s set to %S%% (%s)' % (int(pwm1), brightness, hex(int(brightness/100)*1023).upper()))
        return

def formatHex(data: bytes or int):
    '''Make prettier hex output
    
    `data`: Bytes or Int input
    '''
    if type(data) is bytes:
        output = []
        for i in struct.unpack('%sB' % (len(data)), data):
            if len(hex(i)[2:]) == 1: # Padding
                output.append('0' + hex(i)[2:].upper())
            else:
                output.append(hex(i)[2:].upper())
        return(''.join(output))
    elif type(data) is int:
        return(hex(data)[2:].upper())

# Get our 64-bit Network Address and convert to Little Endian
strNA64 = struct.pack('>i', int.from_bytes(xbee.atcmd('SL'), 'little')) + struct.pack('>i', int.from_bytes(xbee.atcmd('SH'), 'little'))
log(2, 'Our 64-bit Network Address is: %s' % (hex(int.from_bytes(struct.pack('>i', int.from_bytes(xbee.atcmd('SL'), 'little')) + struct.pack('>i', int.from_bytes(xbee.atcmd('SH'), 'little')), 'big'))[2:].upper()))

# Hang out until we're connected, then 
intAIStatus = xbee.atcmd('AI')
while intAIStatus > 0:
    if intAIStatus == 33:
        log(1, 'Network scan complete but no PANs were found')
    elif intAIStatus == 34:
        log(1, 'Network scan complete but our PAN ID wasn\'t found (check SC and ID settings)')
    elif intAIStatus == 35:
        log(1, 'PAN was found but is not in join mode')
    elif intAIStatus == 36:
        log(1, 'No joinable PANs were found')
    elif intAIStatus == 255:
        log(2, 'Network is intializing')
    else:
        log(0, 'Network is in an unknown state (%s), see ZigBee User Guide page 220' % (hex(intAIStatus)))
    hwSleep(1000)

# Now that we're connected, get our 16-bit Network Address
try:
    if strNA16 is not None:
        log(3, 'strNA16 already set')
except NameError:
    strNA16 = struct.pack('<i', xbee.atcmd('MY'), 'little')[:2]
    log(2, 'Our 16-bit Network Address is: %s' % (hex(xbee.atcmd('MY'))[2:]))

# Do a Device Announce so everyone knows we're here
# TODO: Is this nessesary if JN is enabled?
'''try:
    xbee.transmit(
        xbee.ADDR_BROADCAST,
        b'\xAA' + strNA16 + strNA64 + b'\x04',
        cluster = 19
    )
except:
    log(0, xbee.atcmd('AI'))'''

# Main RX Callback Function
def funcRX(data: dict):
    ''' Example Data:
        {
            'cluster': 17,
            'dest_ep': 232,
            'broadcast': False,
            'source_ep': 232,
            'payload': b'Sample payload',
            'profile': 49413,
            'sender_nwk': 63941,
            'sender_eui64': b'\x00\x13\xa2\x00\x92w%`'
        }
    '''

    # Some setup
    byteFrameID = data['payload'][:1]

    '''# Filter out our own packets
    if data['sender_nwk'] == int.from_bytes(strNA16, 'little'):
        return'''

    # Use the Cluster ID to figure out what to do with this data
    intClusterID = data['cluster']
    if intClusterID == 5: # 0x0005 Active Endpoints Request
        log(2, 'Active Endpoint Request from %s' % (formatHex(data['sender_eui64'])))
        listEndpoints = [b'\xAA', b'\x02', b'\x42']
        while True:
            try:
                xbee.transmit(
                    xbee.ADDR_BROADCAST,
                    byteFrameID + b'\x00' + strNA16 + len(listEndpoints).to_bytes(1, 'big') + b''.join(listEndpoints),
                    cluster = 32773
                )
                log(2, 'Sent 8005: %s' % (byteFrameID + b'\x00' + strNA16 + len(listEndpoints).to_bytes(1, 'big') + b''.join(listEndpoints)))
            except OSError as e:
                log(1, 'Failed to send 8005: %s' % (byteFrameID + b'\x00' + strNA16 + len(listEndpoints).to_bytes(1, 'big') + b''.join(listEndpoints)))
                hwSleep(1000)
                continue
            else:
                break
    elif intClusterID == 4: # 0x0004 Simple Descriptor Request
        log(2, 'Simple Descriptor Request from %s' % (formatHex(data['sender_eui64'])))
    elif intClusterID == 146: # 0x0092 I/O Sample Indicator
        return # TODO: Report to HA or something?
    elif intClusterID == 32768: # 0x8000 Network Address Response
        log(3, 'Network Address Response from %s: %s' % (formatHex(data['sender_eui64']), formatHex(data['payload'])))
    elif intClusterID == 32769: # 0x8001 IEEE Address Response
        log(3, 'IEEE Address Response from %s: %s' % (formatHex(data['sender_eui64']), formatHex(data['payload'])))
    else: # Unknown Cluster ID
        log(1, 'Unknown Packet: %s' % (data))

# Set up our callback function
xbee.receive_callback(funcRX)