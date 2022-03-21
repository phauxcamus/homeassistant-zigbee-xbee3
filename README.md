# Introduction
This is a collection of information on how to program a Digi XBee 3 ZigBee module to interface with Home Assistant.

## The Goal
I had come up with the idea that I wanted to create some kind of outdoor light with the following features:
- Battery powered and recharge during the day via solar
- Reasonably useful brightness (1 watt seems to beat most outdoor battery powered lights)
- PIR motion sensor onboard (Bonus: Report this to HA for other automations, like triggering Blue Iris)
- Mesh networking, because Wi-Fi IoT devices suck (ZigBee/Z-Wave, basically)

Recently, Ring has come out with a product that almost does it all -- The [Ring Smart Lighting Family](https://www.amazon.com/stores/page/FBD6D18B-7B2F-4504-8C4C-DD548D0F31C5).  Downsides include (but not limited to):
- Not everyone likes Ring/Amazon
- Requires a special hub to communicate
- Not confirmed if it's meshing wireless
- Not confirmed if it works with HA locally

Thus, I began looking into building my own.  Z-Wave devices are certified and you can't really "DIY" them because of this, so ZigBee it is.  I chose the Digi XBee 3 module as my base because it's already compatible with ZigBee, runs easy-to-develop MicroPython, and is reasonably priced.

## The Problem
The biggest hurdle I've found is that the information is scattered *everywhere*, and it's not any one company's responibility to maintain it.  I've collected information primarily from Digi for the hardware, ZigBee Alliance for the ZDO/ZCL syntax, and a handful of other random websites.

Also, it would seem that nobody uses the MicroPython system for XBee modules, but instead just runs it in Transparent Mode and hooks up an Arduino, ESP or Raspberry Pi to do all the ZigBee traffic and GPIO handling.  I didn't want such a complex system and I'm choosing to do it all in-module on the XBee.

# Structure
This repo is organized for ease of access -- prominant points are listed below:

## main.py
This file is the MicroPython script you can copy to the XBee's filesystem which will auto-run at power on.

## Sample Scripts
A small collection of standalone MicroPython scripts to do various tasks.  The files are commented well for easy digesting.

## PDFs
Reference PDFs from Digi and ZigBee Alliance.  These are very dense with information and can be hard to find what you need, so pertinate information has been copied out and organized better in this repo.