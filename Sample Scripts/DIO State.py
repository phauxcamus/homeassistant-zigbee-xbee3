import xbee, time, struct

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
        return(' '.join(output))
    elif type(data) is int:
        return(hex(data)[2:].upper())

while True:
    data = xbee.receive()
    if data is not None:
        if data['cluster'] == int(0x92): # Data from ourself
            pinstatus = int.from_bytes(data['payload'][4:6], 'big') # Pick out the relavant bytes

            # print('DIO Change: %s' % (''.join(list(('0'*(8-len(bin(int.from_bytes(pinstatus, 'big'))[2:])), bin(int.from_bytes(pinstatus, 'big'))[2:]))))) # Output new state
            print('DIO Change: %s' % (formatHex(pinstatus)))

            # Bonus: Toggle PWM0 if DIO4 is high
            if pinstatus == 128:
                xbee.atcmd('M0', 0x000)
            elif pinstatus == 144:
                xbee.atcmd('M0', 0x3FF)