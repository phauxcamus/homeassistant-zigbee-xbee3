# 0x0005 Active Endpoints Request
This packet is sent by the Coordinator after we have sent a `0x0013` Device Announce broadcast.  A [`0x8005` Active Endpoints Response](#0x8005-active-endpoints-response) is broadcasted back.

## Bytes (3):
|Name                      |Bytes|Example        |
|:-------------------------|:----|:--------------|
|Frame ID                  |1    |*Arbitrary*    |
|Our 16-bit Network Address|2    |AT Command `MY`|

## Sample
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

# 0x0013 Device Announce
## Bytes (12):
|Name                  |Bytes|Example               |
|:---------------------|:----|:---------------------|
|Frame ID              |1    |*Arbitrary*           |
|16-bit Network Address|2    |AT Command `MY`       |
|64-bit Network Address|8    |AT Command `SH` + `SL`|
|Capability            |1    |Receive On (`0x04`)   |

Currently the Capability byte is always `0x04` for Receive On.

# 0x0092 XBee I/O Sample
Sent out automatically based on the `IR` polling rate.  The Destination address is defined by `DH` and `DL`.

## Bytes (Variable):
|Name            |Bytes   |Example                                    |
|:---------------|:-------|:------------------------------------------|
|Sample Set      |1       |Number of samples (always `0x01`)          |
|DIO Pins Sampled|2       |Bit mask of DIO pins sampled               |
|AD Pins Sampled |1       |Bit mask of AD pins sampled                |
|DIO Data        |2       |Bit mask of DIO pins status (high or low)  |
|AD Data         |Variable|Variable list of 2 bytes per AD pin sampled|

The AD Data section may be omitted if AD Pins Sampled is `0x00`.  

## Sample
In the sample below, a PIR sensor's output was attached to DIO4 and powered via DIO7. Bytes 2-3 show DIO Pins 4 and 7 being selected for polling (all others are disabled), and the bytes 5-6 report their status: bit 4 is low (no motion), and bit 7 is high (supply power to the sensor).  There is no AD Data because AD Pins Sampled is `0x00` (all AD pins are disabled or in DIO mode).

```python
{
    'profile': 49413,
    'dest_ep': 232,
    'broadcast': False,
    'sender_nwk': 24516,
    'source_ep': 232,
    'payload': b'\x01\x00\x90\x00\x00\x80',
    'sender_eui64': b'\x00\x13\xa2\x00A\x94\n,',
    'cluster': 146
}
```

# 0x8004 Simple Descriptor Response
Send this back when the Coordinator asks us to describe an Endpoint (one at a time).

## Bytes (Variable):
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

# 0x8005 Active Endpoints Response
This will be sent back when we get a `0x0005` Active Endpoints Request from the Coordinator (Interviewing has started).  You will need to get the Frame ID from the Request packet and respond with that.

## Bytes (Variable):
|Name                      |Bytes   |Example                |
|:-------------------------|:-------|:----------------------|
|Frame ID                  |1       |From the Request packet|
|Status                    |1       |OK (`0x00`)            |
|16-bit Network Address    |2       |AT Command `MY`        |
|Endpoint Count            |1       |                       |
|List of Endpoint Addresses|Variable|                       |

