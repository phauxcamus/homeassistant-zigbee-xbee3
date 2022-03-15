# Reference Websites
Digi Xbee3 ZigBee Documentation:  https://www.digi.com/resources/documentation/digidocs/90001539/ (PDF downloaded into this repo [here](90001539%20XBee3.pdf))

Archive.org of someone getting an XBee connected with SmartThings: https://web.archive.org/web/20180218010916/https://www.falco.co.nz/electronic-projects/xbee-to-smartthings/

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
xbee.transmit(
    dest    = xbee.ADDR_BROADCAST,
    cluster = b'\x00\x13',
    payload = b'\xAA\x00\xF1\x2C\x0A\x94\x41\x00\xA2\x13\x00\x04'
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