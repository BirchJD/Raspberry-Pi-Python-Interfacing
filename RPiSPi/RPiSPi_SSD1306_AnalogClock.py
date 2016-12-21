#!/usr/bin/python2

# RPiSPi_SSD1306_AnalogClock - Python Example For RPiSPi Driver Using SSD1306
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
#/* RPiSPi_SSD1306_AnalogClock                                               */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2016-12-20 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Python Example For RPiSPi Driver Using SSD1306 Display.                  */
#/****************************************************************************/


import time
import math
import datetime
import curses
import struct


SSD1306_INIT                      = "/dev/RPiSPi_10010_000_7_0_SSD1306_INIT"
SSD1306_WRITE                     = "/dev/RPiSPi_10010_000_7_1_SSD1306_WRITE"

SPI_DEV_CMD_SSD1306_INIT          = 0
SPI_DEV_CMD_SSD1306_WRITE         = 1
SPI_DEV_CMD_SSD1306_CURSOR_POS    = 2
SPI_DEV_CMD_SSD1306_ON            = 3
SPI_DEV_CMD_SSD1306_OFF           = 4
SPI_DEV_CMD_SSD1306_INVERSE       = 5
SPI_DEV_CMD_SSD1306_NON_INVERSE   = 6
SPI_DEV_CMD_SSD1306_CONTRAST      = 7
SPI_DEV_PRC_SSD1306_CLS           = 8
SPI_DEV_PRC_SSD1306_FILL_RANDOM   = 9
SPI_DEV_PRC_SSD1306_PRINT         = 10
SPI_DEV_PRC_SSD1306_PLOT          = 11
SPI_DEV_PRC_SSD1306_LINE          = 12
SPI_DEV_PRC_SSD1306_BOX           = 13
SPI_DEV_PRC_SSD1306_BOX_FILL      = 14
SPI_DEV_PRC_SSD1306_CIRCLE        = 15
SPI_DEV_PRC_SSD1306_CIRCLE_FILL   = 16
SPI_DEV_PRC_SSD1306_UPDATE        = 17



def DoDisplay(*Args):
   Message = ""
   for Count in range(len(Args)):
      if isinstance(Args[Count], str):
         Message += Args[Count]
      else:
         Message += struct.pack('I', Args[Count])
   File.write(Message)


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

WriteGPIO(SSD1306_INIT, SPI_DEV_CMD_SSD1306_INIT)
File = open(SSD1306_WRITE, 'wb', 0)

DoDisplay(SPI_DEV_CMD_SSD1306_ON)
DoDisplay(SPI_DEV_CMD_SSD1306_CONTRAST, 127)
DoDisplay(SPI_DEV_PRC_SSD1306_CLS)

LastHour = 0
LastMinute = 0
LastSecond = 0
LastMicrosecond = 0
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

#  /******************************/
# /* Get current time and date. */
#/******************************/
   Now = datetime.datetime.now()

#  /********************/
# /* Erase last time. */
#/********************/
   DoDisplay(SPI_DEV_PRC_SSD1306_LINE, 32, 32, 32 + math.cos((2 * 3.142 * (LastHour + LastMinute / 60.0) / 12) - 3.142 / 2) * 18, 32 + math.sin((2 * 3.142 * (LastHour + LastMinute / 60.0) / 12) - 3.142 / 2) * 18, 0)
   DoDisplay(SPI_DEV_PRC_SSD1306_LINE, 32, 32, 32 + math.cos((2 * 3.142 * (LastMinute + LastSecond / 60.0) / 60) - 3.142 / 2) * 27, 32 + math.sin((2 * 3.142 * (LastMinute + LastSecond / 60.0) / 60) - 3.142 / 2) * 27, 0)
   DoDisplay(SPI_DEV_PRC_SSD1306_LINE, 32, 32, 32 + math.cos((2 * 3.142 * (LastSecond + LastMicrosecond / 1000000.0) / 60) - 3.142 / 2) * 30, 32 + math.sin((2 * 3.142 * (LastSecond + LastMicrosecond / 1000000.0) / 60) - 3.142 / 2) * 30, 0)

#  /**************************/
# /* Remember current time. */
#/**************************/
   LastHour = Now.hour
   LastMinute = Now.minute
   LastSecond = Now.second
   LastMicrosecond = Now.microsecond

#  /*************************/
# /* Display current time. */
#/*************************/
   DoDisplay(SPI_DEV_PRC_SSD1306_LINE, 32, 32, 32 + math.cos((2 * 3.142 * (LastHour + LastMinute / 60.0) / 12) - 3.142 / 2) * 18, 32 + math.sin((2 * 3.142 * (LastHour + LastMinute / 60.0) / 12) - 3.142 / 2) * 18, 1)
   DoDisplay(SPI_DEV_PRC_SSD1306_LINE, 32, 32, 32 + math.cos((2 * 3.142 * (LastMinute + LastSecond / 60.0) / 60) - 3.142 / 2) * 27, 32 + math.sin((2 * 3.142 * (LastMinute + LastSecond / 60.0) / 60) - 3.142 / 2) * 27, 1)
   DoDisplay(SPI_DEV_PRC_SSD1306_LINE, 32, 32, 32 + math.cos((2 * 3.142 * (LastSecond + LastMicrosecond / 1000000.0) / 60) - 3.142 / 2) * 30, 32 + math.sin((2 * 3.142 * (LastSecond + LastMicrosecond / 1000000.0) / 60) - 3.142 / 2) * 30, 1)

#  /*****************/
# /* Display date. */
#/*****************/
   DoDisplay(SPI_DEV_PRC_SSD1306_PRINT, 81, 6, 2, 1, Now.strftime("%a").upper())
   DoDisplay(SPI_DEV_PRC_SSD1306_PRINT, 87, 20, 2, 1, Now.strftime("%d"))
   DoDisplay(SPI_DEV_PRC_SSD1306_PRINT, 81, 35, 2, 1, Now.strftime("%b").upper())
   DoDisplay(SPI_DEV_PRC_SSD1306_PRINT, 76, 50, 2, 1, Now.strftime("%Y"))

#  /********************/
# /* Display borders. */
#/********************/
   for Count in range(0, 60, 5):
      DoDisplay(SPI_DEV_PRC_SSD1306_CIRCLE, 32 + math.cos(2 * 3.142 * Count / 60) * 25, 32 + math.sin(2 * 3.142 * Count / 60) * 25, 2, 1)

   DoDisplay(SPI_DEV_PRC_SSD1306_CIRCLE, 32, 32, 31, 1)
   DoDisplay(SPI_DEV_PRC_SSD1306_BOX, 70, 0, 127, 63, 1)

#  /*******************/
# /* Update display. */
#/*******************/
   DoDisplay(SPI_DEV_PRC_SSD1306_UPDATE)


DoDisplay(SPI_DEV_CMD_SSD1306_OFF)

File.close()

#  /*********************/
# /* Exit application. */
#/*********************/
curses.endwin()

