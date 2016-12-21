#!/usr/bin/python2

# RPiSPi_MCP3008 - Python Example For RPiSPi Driver Using MCP3008 A-D Converter
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
#/* RPiSPi_MCP3008                                                           */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2016-11-02 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Python Example For RPiSPi Driver Using MCP3008 A-D Converter.            */
#/****************************************************************************/


import sys
import time
import datetime
import curses
import struct


MCP3008_READ0 = "/dev/RPiSPi_00000_000_0_2_MCP3008_READ0"
MCP3008_READ1 = "/dev/RPiSPi_00000_000_0_3_MCP3008_READ1"
MCP3008_READ2 = "/dev/RPiSPi_00000_000_0_4_MCP3008_READ2"
MCP3008_READ3 = "/dev/RPiSPi_00000_000_0_5_MCP3008_READ3"
MCP3008_READ4 = "/dev/RPiSPi_00000_000_0_6_MCP3008_READ4"
MCP3008_READ5 = "/dev/RPiSPi_00000_000_0_7_MCP3008_READ5"
MCP3008_READ6 = "/dev/RPiSPi_00000_000_0_8_MCP3008_READ6"
MCP3008_READ7 = "/dev/RPiSPi_00000_000_0_9_MCP3008_READ7"



def ReadAD(DevFile):
   File = open(DevFile, 'rb', 0)
   Data = File.read(4)
   File.close()
   return struct.unpack("<%dI" % (len(Data) // 4), Data)[0]



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

   Value0 = ReadAD(MCP3008_READ0)
   Value1 = ReadAD(MCP3008_READ1)
   Value2 = ReadAD(MCP3008_READ2)
   Value3 = ReadAD(MCP3008_READ3)
   Value4 = ReadAD(MCP3008_READ4)
   Value5 = ReadAD(MCP3008_READ5)
   Value6 = ReadAD(MCP3008_READ6)
   Value7 = ReadAD(MCP3008_READ7)

   Now = datetime.datetime.now()
   print(Now.strftime("%Y-%m-%d %H:%M:%S") + "   A-D_[0]=" + str(Value0) + "   A-D_[1]=" + str(Value1) + "   A-D_[2]=" + str(Value2) + "   A-D_[3]=" + str(Value3) + "\r")
   print(Now.strftime("%Y-%m-%d %H:%M:%S") + "   A-D_[4]=" + str(Value4) + "   A-D_[5]=" + str(Value5) + "   A-D_[6]=" + str(Value6) + "   A-D_[7]=" + str(Value7) + "\r")



#  /*********************/
# /* Exit application. */
#/*********************/
curses.endwin()

