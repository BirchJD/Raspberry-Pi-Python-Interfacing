#!/usr/bin/python2

# RPiSPi_RAW - Python Example For RPiSPi Driver Using RAW SPI Device Mode
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
#/* RPiSPi_RAW                                                               */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2016-11-02 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Python Example For RPiSPi Driver Using RAW SPI Device Mode to            */
#/* communicate with an MCP3008 A-D Converter.                               */
#/****************************************************************************/


import sys
import time
import datetime
import curses
import struct


def ReadRAW(DevFile):
   File = open(DevFile, 'rb', 0)
   Data = File.read(256 * 4)
   File.close()
   return list(struct.unpack("<%dI" % (len(Data) // 4), Data))


def WriteRAW(DevFile, *Args):
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

   WriteRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW", 0x01, 0x80, 0x00)
   Values = ReadRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW")
   Value0 = 256 * (Values[1] & 0x03) + Values[2]

   WriteRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW", 0x01, 0x90, 0x00)
   Values = ReadRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW")
   Value1 = 256 * (Values[1] & 0x03) + Values[2]

   WriteRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW", 0x01, 0xA0, 0x00)
   Values = ReadRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW")
   Value2 = 256 * (Values[1] & 0x03) + Values[2]

   WriteRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW", 0x01, 0xB0, 0x00)
   Values = ReadRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW")
   Value3 = 256 * (Values[1] & 0x03) + Values[2]

   WriteRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW", 0x01, 0xC0, 0x00)
   Values = ReadRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW")
   Value4 = 256 * (Values[1] & 0x03) + Values[2]

   WriteRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW", 0x01, 0xD0, 0x00)
   Values = ReadRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW")
   Value5 = 256 * (Values[1] & 0x03) + Values[2]

   WriteRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW", 0x01, 0xE0, 0x00)
   Values = ReadRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW")
   Value6 = 256 * (Values[1] & 0x03) + Values[2]

   WriteRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW", 0x01, 0xF0, 0x00)
   Values = ReadRAW("/dev/RPiSPi_001_000_1_0_SPI_RAW_REG_RAW")
   Value7 = 256 * (Values[1] & 0x03) + Values[2]

   Now = datetime.datetime.now()
   print(Now.strftime("%Y-%m-%d %H:%M:%S") + "   A-D_[0]=" + str(Value0) + "   A-D_[1]=" + str(Value1) + "   A-D_[2]=" + str(Value2) + "   A-D_[3]=" + str(Value3) + "\r")
   print(Now.strftime("%Y-%m-%d %H:%M:%S") + "   A-D_[4]=" + str(Value4) + "   A-D_[5]=" + str(Value5) + "   A-D_[6]=" + str(Value6) + "   A-D_[7]=" + str(Value7) + "\r")



#  /*********************/
# /* Exit application. */
#/*********************/
curses.endwin()

