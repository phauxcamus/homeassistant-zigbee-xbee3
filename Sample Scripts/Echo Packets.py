import xbee, time, struct

def formatHex(data: bytes or int):
    '''Make prettier hex output
    
    `data`: Bytes or Int input
    '''
    if type(data) is bytes:
        output = []
        for i in struct.unpack('%sB' % (len(data)), data):
            output.append(hex(i)[2:].upper())
        return(''.join(output))
    elif type(data) is int:
        return(hex(data)[2:].upper())

while True:
    data = xbee.receive()
    if data is not None:
        '''
            receive() outputs a simple dictionary that you can just print:
                {
                    'profile': 0,
                    'dest_ep': 0,
                    'broadcast': False,
                    'sender_nwk': 0,
                    'source_ep': 0,
                    'payload': b'#\xc4_',
                    'sender_eui64': b'\x00\ro\x00\x12M\r@',
                    'cluster': 5
                }

            ...But I decided to customize it and only output what I need to see:
        '''
        print('[%s] From: %s, Profile: %s, Cluster: %s, Payload: %s' % (int(time.ticks_ms()/1000), formatHex(data['sender_eui64']), formatHex(data['profile']), formatHex(data['cluster']), formatHex(data['payload'])))