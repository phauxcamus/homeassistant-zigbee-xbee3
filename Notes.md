# Reference Websites
Digi Xbee3 ZigBee Documentation:  https://www.digi.com/resources/documentation/digidocs/90001539/ (PDF downloaded into this repo [here](90001539%20XBee3.pdf))

Archive.org of someone getting an XBee connected with SmartThings: https://web.archive.org/web/20180218010916/https://www.falco.co.nz/electronic-projects/xbee-to-smartthings/

# Packets we need to construct
These are the packets we need to build in order to communicate with the Coordinator.  The list is incomplete but growing!

Note:  All addresses are Little Endian.

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