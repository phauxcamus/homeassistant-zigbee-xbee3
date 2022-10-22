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

bytesPayloadOld = b''
while True:
    data = xbee.receive()
    if data is not None:
        bytesPayload = data['payload']
        if data['cluster'] == int(0x92): # Data from ourself
            if bytesPayload == bytesPayloadOld:
                print('[%s] Same Data' % (int(time.ticks_ms()/1000)))
                continue
            print('[%s] IO Data:' % (int(time.ticks_ms()/1000)))
            print('    Raw Data: %s' % (formatHex(bytesPayload)))
            print('    DIO Monitored: %s' % (formatHex(bytesPayload[1:3])))
            print('    DIO State: %s / %s' % (formatHex(bytesPayload[4:6]), int.from_bytes(bytesPayload[4:6], 'big')))
            print('    AIO Monitored: %s' % (formatHex(bytesPayload[3])))
            print('    AIO State: %s' % (formatHex(bytesPayload[6:])))



            # Save our new data for later comparison
            bytesPayloadOld = bytesPayload