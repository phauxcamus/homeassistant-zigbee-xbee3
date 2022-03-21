As of firmware 100D, these are the settings used (all others are default):

|Parameter|Description|Value|
|:-|:-|:-|
|ID|Extended PAN ID|*Your ZigBee network's PAN ID*|
|ZS|Zigbee Stack Profile|2 *(Zigbee-PRO)*|
|JN|Join Notification|1 *(Enabled)*|
|NI|Node Identifier|*Any Description*|
|NO|Node Discovery Options|3|
|EE|Encryption Enable|1 *(Enabled)*|
|EO|Encryption Options|1 *(Transmit NWK Keys in the clear)*|
|SC|Scan Channels|FFFF *(If you know the specific channel for your PAN, use that instead)*|
|AP|API Enable|4 *(MicroPython REPL)*|
|AO|API Output Mode|7 *(ZDO Passthrough)*|
|BD|UART Baud Rate|7 *(115200)*|
|D5|DIO5/Association LED Configuration|0 *(Disabled)*|
|P0|DIO10/PWM0 Configuration|2 *(PWM Output)*|
|P1|DIO11 Configuration|2 *(PWM Output)*|