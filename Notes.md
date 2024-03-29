# Reference Websites
Digi Xbee3 ZigBee Documentation:  https://www.digi.com/resources/documentation/digidocs/90001539/ (PDF downloaded into this repo [here](90001539%20XBee3.pdf))

Archive.org of someone getting an XBee connected with SmartThings: https://web.archive.org/web/20180218010916/https://www.falco.co.nz/electronic-projects/xbee-to-smartthings/

Profiles and Device ID Types:  https://www.rfwireless-world.com/Terminology/Zigbee-Profile-ID-list.html

Some Clusters:  https://www.rfwireless-world.com/Terminology/Zigbee-Cluster-ID-list.html

# Packets we need to construct
These are the packets we need to build in order to communicate with the Coordinator.  The list is incomplete but growing!

Note:  All addresses are Little Endian.

## 0x0013 Device Announce
Bytes (12 total):
|Name                  |Bytes|Example               |
|:---------------------|:----|:---------------------|
|Frame ID              |1    |*Arbitrary*           |
|16-bit Network Address|2    |AT Command `MY`       |
|64-bit Network Address|8    |AT Command `SH` + `SL`|
|Capability            |1    |Receive On (`0x04`)   |

Currently the Capability byte is always `0x04` for Receive On.  I don't know why it's that, nor do I know what other options there are.

Example Transmit Command:
```python
byteNA16 = b'\x00\xF1'
byteNA64 = b'\x2C\x0A\x94\x41\x00\xA2\x13\x00'
xbee.transmit(
    dest    = xbee.ADDR_BROADCAST,
    cluster = b'\x00\x13',
    payload = b'\xAA' + strNA16 + strNA64 + b'\x04'
)
```

## 0x8005 Active Endpoints Response
This will be sent back when we get a 0x0005 Active Endpoints Request from the Coordinator (Interviewing has started).  You will need to get the Frame ID from the Request packet and respond with that.

Bytes (Variable Length):
|Name                      |Bytes   |Example                |
|:-------------------------|:-------|:----------------------|
|Frame ID                  |1       |From the Request packet|
|Status                    |1       |OK (`0x00`)            |
|16-bit Network Address    |2       |AT Command `MY`        |
|Endpoint Count            |1       |                       |
|List of Endpoint Addresses|Variable|                       |

Example Transmit Command:
```python
byteNA16 = b'\x00\xF1'
byteReqID = b'\xDE'
listEndpoints = [b'\xAA', b'\x02', b'\x42']
xbee.transmit(
    dest = xbee.ADDR_BROADCAST,
    cluster = b'\x80\x05',
    payload = byteReqID + b'\x00' + byteNA16 + len(listEndpoints).to_bytes(1, 'big') + b''.join(listEndpoints)
)
```

## 0x8004 Simple Descriptor Response
Send this back when the Coordinator asks us to describe an Endpoint (one at a time).

Bytes (Variable Length):
Name                                 |Bytes   |Example                                                     |
|:-----------------------------------|:-------|:-----------------------------------------------------------|
|Frame ID                            |1       |From the Request packet                                     |
|Status                              |1       |OK (`0x00`)                                                 |
|16-bit Network Address              |2       |AT Command `MY`                                             |
|Sum of bytes following this one     |1       |                                                            |
|Endpoint ID                         |1       |From the Request packet                                     |
|Endpoint Profile                    |2       |Home Automation (`0x0401`)                                  |
|Endpoint Type                       |2       |Binary (`0x0200`)                                           |
|Version Number                      |1       |`0x30`                                                      |
|Sum of Cluster Types Accepted       |1       |                                                            |
|List of Cluster Types Accepted      |Variable|`0x0000` for Basic, `0x0300` for ID, and `0x0600` for On/Off|
|Sum of Cluster Types Transmitted    |1       |                                                            |
|List of Cluster Types Transmitted   |Variable|                                                            |

Both Lists can be skipped if there's none (Sum is 0)

I'm not sure what other Endpoint Types are available, and what Clusters Types can be accepted or transmitted, but it's worth looking into soon.

Example Transmit Command:
```python
byteNA16 = b'\x00\xF1'
byteReqID = b'\xDE'
byteEndpointID = b'\xAA'
listClustersRX = [b'\x00\x00', b'\x03\x00', b'\x06\x00']
listClustersTX = []
bytesData = byteEndpointID + b'\x04\x01\x02\x00\x30' + len(listClustersRX).to_bytes(1, 'big') + b''.join(listClustersRX) + len(listClustersTX).to_bytes(1, 'big') + b''.join(listClustersTX)
xbee.transmit(
    dest    = xbee.ADDR_BROADCAST,
    cluster = b'\x80\x05',
    payload = byteReqID + b'\x00' + byteNA16 + len(bytesData).to_bytes(1, 'big') + bytesData
)
```

# Snippets
Packets received look like this (example below is of Cluster 0x0005 from the Coordinator):
```python
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
```