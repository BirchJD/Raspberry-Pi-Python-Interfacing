#!/usr/bin/python2

# RPiSPi_MCP3002 - Python Example For RPiSPi Driver Using MCP3002 A-D Converter
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
#/* RPiSPi_MCP3002                                                           */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2016-11-02 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Python Example For RPiSPi Driver Using MCP3002 A-D Converter.            */
#/****************************************************************************/


import sys
import time
import datetime
import curses
import struct


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

   Value0 = ReadAD("/dev/RPiSPi_0100_000_0_2_MCP3002_READ0")
   Value1 = ReadAD("/dev/RPiSPi_0100_000_0_3_MCP3002_READ1")

   Now = datetime.datetime.now()
   print(Now.strftime("%Y-%m-%d %H:%M:%S") + "   A-D_[0]=" + str(Value0) + "   A-D_[1]=" + str(Value1) + "\r")


#  /*********************/
# /* Exit application. */
#/*********************/
curses.endwin()

