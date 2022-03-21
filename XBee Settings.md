As of firmware 100D, these are the settings used (all others are default):

|Parameter|Description                       |Value                                                                       |
|:--------|:---------------------------------|:---------------------------------------------------------------------------|
|AO       |API Output Mode                   |`0x07` *(ZDO Passthrough)*                                                  |
|AP       |API Enable                        |`0x04` *(MicroPython REPL)*                                                 |
|BD       |UART Baud Rate                    |`0x07` *(115200)*                                                           |
|D5       |DIO5/Association LED Configuration|`0x00` *(Disabled)*                                                         |
|EE       |Encryption Enable                 |`0x01` *(Enabled)*                                                          |
|EO       |Encryption Options                |`0x01` *(Transmit NWK Keys in the clear)*                                   |
|ID       |Extended PAN ID                   |*Your ZigBee network's PAN ID*                                              |
|JN       |Join Notification                 |`0x01` *(Enabled)*                                                          |
|NI       |Node Identifier                   |*Any Description*                                                           |
|NO       |Node Discovery Options            |`0x03`                                                                      |
|P0       |DIO10/PWM0 Configuration          |`0x02` *(PWM Output)*                                                       |
|P1       |DIO11 Configuration               |`0x02` *(PWM Output)*                                                       |
|SC       |Scan Channels                     |`0xFFFF` *(If you know the specific channel for your PAN, use that instead)*|
|ZS       |Zigbee Stack Profile              |`0x02` *(Zigbee-PRO)*                                                       |