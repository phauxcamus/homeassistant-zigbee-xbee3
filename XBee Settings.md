As of firmware 100D, these are the settings used (all others are default):

|Parameter|Description                       |Value                                                                       |
|:--------|:---------------------------------|:---------------------------------------------------------------------------|
|AO       |API Output Mode                   |`0x07` *(ZDO Passthrough)*                                                  |
|AP       |API Enable                        |`0x04` *(MicroPython REPL)*                                                 |
|D1       |DIO1/AD1/SPI_nATTN Configuration  |`0x03` *(Digital Input)*                                                    |
|D6       |DIO6/RTS Configuration            |`0x01` *(RTS flow control)*                                                 |
|DH       |Destination Address High          |*Set to the value of `SH` to loop back the Sample data enabled by `IR`*     |
|DL       |Destination Address Low           |*Set to the value of `SL` to loop back the Sample data enabled by `IR`*     |
|EE       |Encryption Enable                 |`0x01` *(Enabled)*                                                          |  0
|EO       |Encryption Options                |`0x01` *(Transmit NWK Keys in the clear)*                                   | 11
|ID       |Extended PAN ID                   |*Your ZigBee network's PAN ID*                                              |
|IC       |Digital IO Change Detection       |*Bit mask of which pins to monitor for changes*                             |
|JN       |Join Notification                 |`0x01` *(Enabled)*                                                          |
|NI       |Node Identifier                   |*Any Description*                                                           |
|NO       |Node Discovery Options            |`0x03`                                                                      |
|P1       |DIO11 Configuration               |`0x02` *(PWM Output)*                                                       |
|SC       |Scan Channels                     |`0xFFFF` *(If you know the specific channel for your PAN, use that instead)*|
|ZS       |Zigbee Stack Profile              |`0x02` *(Zigbee-PRO)*                                                       |