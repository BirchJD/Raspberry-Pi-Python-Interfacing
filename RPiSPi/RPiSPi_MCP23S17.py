#!/usr/bin/python2

# RPiSPi_MCP23S17 - Python Example For RPiSPi Driver For MCP23S17 GPIO Expander
# Copyright (C) 2016 Jason Birch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#/****************************************************************************/
#/* RPiSPi_MCP23S17                                                          */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2016-11-02 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Python Example For RPiSPi Driver Using MCP23S17 GPIO Expander.           */
#/****************************************************************************/


import sys
import time
import datetime
import curses
import struct

MCP23S17_INIT_0    = "/dev/RPiSPi_00011_000_3_0_MCP23S17_INIT"
MCP23S17_WRITE_0   = "/dev/RPiSPi_00011_000_3_1_MCP23S17_WRITE"
MCP23S17_READ_0    = "/dev/RPiSPi_00011_000_3_2_MCP23S17_READ"
MCP23S17_IODIR_0   = "/dev/RPiSPi_00011_000_3_3_MCP23S17_IODIR"
MCP23S17_IPOL_0    = "/dev/RPiSPi_00011_000_3_4_MCP23S17_IPOL"
MCP23S17_GPINTEN_0 = "/dev/RPiSPi_00011_000_3_5_MCP23S17_GPINTEN"
MCP23S17_DEFVAL_0  = "/dev/RPiSPi_00011_000_3_6_MCP23S17_DEFVAL"
MCP23S17_INTCON_0  = "/dev/RPiSPi_00011_000_3_7_MCP23S17_INTCON"
MCP23S17_GPPU_0    = "/dev/RPiSPi_00011_000_3_8_MCP23S17_GPPU"

MCP23S17_INIT_1    = "/dev/RPiSPi_00011_001_4_0_MCP23S17_INIT"
MCP23S17_READ_1    = "/dev/RPiSPi_00011_001_4_2_MCP23S17_READ"
MCP23S17_IODIR_1   = "/dev/RPiSPi_00011_001_4_3_MCP23S17_IODIR"
MCP23S17_IPOL_1    = "/dev/RPiSPi_00011_001_4_4_MCP23S17_IPOL"
MCP23S17_GPINTEN_1 = "/dev/RPiSPi_00011_001_4_5_MCP23S17_GPINTEN"
MCP23S17_DEFVAL_1  = "/dev/RPiSPi_00011_001_4_6_MCP23S17_DEFVAL"
MCP23S17_INTCON_1  = "/dev/RPiSPi_00011_001_4_7_MCP23S17_INTCON"
MCP23S17_GPPU_1    = "/dev/RPiSPi_00011_001_4_8_MCP23S17_GPPU"



SPI_DEV_CMD_MCP23S17_INIT         = 0
SPI_DEV_CMD_MCP23S17_WRITE        = 1
SPI_DEV_CMD_MCP23S17_READ         = 2
# IODIR - I/O DIRECTION REGISTER - 0=OUTPUT, 1=INPUT
SPI_DEV_CMD_MCP23S17_IODIR        = 3
# IPOL - INPUT POLARITY PORT REGISTER
SPI_DEV_CMD_MCP23S17_IPOL         = 4
# GPINTEN - INTERRUPT-ON-CHANGE PINS
SPI_DEV_CMD_MCP23S17_GPINTEN      = 5
# DEFVAL - DEFAULT VALUE REGISTER
SPI_DEV_CMD_MCP23S17_DEFVAL       = 6
# INTCON - INTERRUPT-ON-CHANGE CONTROL REGISTER
SPI_DEV_CMD_MCP23S17_INTCON       = 7
# GPPU - GPIO PULL-UP RESISTOR REGISTER
SPI_DEV_CMD_MCP23S17_GPPU         = 8
# INTF - INTERRUPT FLAG REGISTER
SPI_DEV_CMD_MCP23S17_INTF         = 9
# INTCAP - INTERRUPT CAPTURED VALUE FOR PORT REGISTER
SPI_DEV_CMD_MCP23S17_INTCAP       = 10



def ReadGPIO(DevFile):
   File = open(DevFile, 'rb', 0)
   Data = File.read(4)
   File.close()
   return struct.unpack("<%dI" % (len(Data) // 4), Data)[0]


def WriteGPIO(DevFile, *Args):
   Message = ""
   for Count in range(len(Args)):
      if isinstance(Args[Count], str):
         Message += Args[Count]
      else:
         Message += struct.pack('I', Args[Count])
   File = open(DevFile, 'wb', 0)
   File.write(Message)
   File.close()



#  /*********************************************************/
# /* Configure the console so key presses can be captured. */
#/*********************************************************/
curses.initscr()
curses.noecho()
window = curses.newwin(80, 25)
window.nodelay(1)
window.timeout(0)

WriteGPIO(MCP23S17_INIT_0, SPI_DEV_CMD_MCP23S17_INIT)
WriteGPIO(MCP23S17_IODIR_0, 0xFF00)
WriteGPIO(MCP23S17_IPOL_0, 0xFF00)
WriteGPIO(MCP23S17_GPINTEN_0, 0x0000)
WriteGPIO(MCP23S17_DEFVAL_0, 0x0000)
WriteGPIO(MCP23S17_INTCON_0, 0x0000)
WriteGPIO(MCP23S17_GPPU_0, 0xFF00)

WriteGPIO(MCP23S17_INIT_1, SPI_DEV_CMD_MCP23S17_INIT)
WriteGPIO(MCP23S17_IODIR_1, 0xFFFF)
WriteGPIO(MCP23S17_IPOL_1, 0x0000)
WriteGPIO(MCP23S17_GPINTEN_1, 0x0000)
WriteGPIO(MCP23S17_DEFVAL_1, 0x0000)
WriteGPIO(MCP23S17_INTCON_1, 0x0000)
WriteGPIO(MCP23S17_GPPU_1, 0xF00F)

OutValue = 0;
ExitFlag = False
while ExitFlag == False:
#  /**********************************************/
# /* Process main application loop every 200ms. */
#/**********************************************/
   curses.napms(200)

#  /*************************/
# /* Get a user key press. */
#/*************************/
   ThisKey = window.getch()

#  /****************************************************/
# /* If a key has been pressed, exit the application. */
#/****************************************************/
   if ThisKey > -1:
      ExitFlag = True

   OutValue /= 2
   if OutValue == 0:
      OutValue = 0x80;

   WriteGPIO(MCP23S17_WRITE_0, (~OutValue) & 0xFF)

   Now = datetime.datetime.now()
   Value0 = ReadGPIO(MCP23S17_READ_0)
   Value1 = ReadGPIO(MCP23S17_READ_1)
   print(Now.strftime("%Y-%m-%d %H:%M:%S") + "   GPIO0:  " + format(Value0, '016b') + " - GPIO1:  " + format(Value1, '016b') + "\r")



#  /*********************/
# /* Exit application. */
#/*********************/
curses.endwin()

