#!/usr/bin/python2

# RPiSPi_SSD1306 - Python Example For RPiSPi Driver Using SSD1306 Display
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
#/* RPiSPi_SSD1306                                                           */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2016-11-02 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Python Example For RPiSPi Driver Using SSD1306 Display.                  */
#/****************************************************************************/


import time
import datetime
import curses
import struct


SSD1306_INIT                      = "/dev/RPiSPi_10001_000_6_0_SSD1306_INIT"
SSD1306_WRITE                     = "/dev/RPiSPi_10001_000_6_1_SSD1306_WRITE"

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


def ScrollMessage(XPos, YPos, XSize, YSize, Message):
   DoDisplay(SPI_DEV_PRC_SSD1306_BOX_FILL, 0, YPos, XSize * 6, YPos + YSize * 8, 0)
   DoDisplay(SPI_DEV_PRC_SSD1306_PRINT, XPos, YPos, XSize, YSize, Message)
   WrapMessage = Message[int(((len(Message) + 1) * 6 * XSize - XPos) / (XSize * 6)):]
   DoDisplay(SPI_DEV_PRC_SSD1306_PRINT, (XPos - 1) % (XSize * 6), YPos, XSize, YSize, WrapMessage)


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

Pos1 = 0
Pos2 = 0
Message2 = " <<<<< Scroll Message Left <<<<< "
Pos3 = 0
Message3 = " >>>>> Scroll Message Right >>>>> "

ExitFlag = False
while ExitFlag == False:
#  /**********************************************/
# /* Process main application loop every 200ms. */
#/**********************************************/
   curses.napms(100)

#  /*************************/
# /* Get a user key press. */
#/*************************/
   ThisKey = window.getch()

#  /****************************************************/
# /* If a key has been pressed, exit the application. */
#/****************************************************/
   if ThisKey > -1:
      ExitFlag = True

   Now = datetime.datetime.now()
   Message1 = Now.strftime(" %Y-%m-%d %H:%M:%S ")

   ScrollMessage(Pos1, 0, 1, 2, Message1)
   ScrollMessage(Pos2, 25, 2, 2, Message2)
   ScrollMessage(Pos3, 50, 2, 2, Message3)

   DoDisplay(SPI_DEV_PRC_SSD1306_UPDATE)

   Pos1 += 2
   if Pos1 >= len(Message1) * 6 * 1:
      Pos1 = 0

   Pos2 -= 2
   if Pos2 <= 0:
      Pos2 = len(Message2) * 6 * 2

   Pos3 += 2
   if Pos3 >= len(Message3) * 6 * 2:
      Pos3 = 0



DoDisplay(SPI_DEV_CMD_SSD1306_OFF)

File.close()

#  /*********************/
# /* Exit application. */
#/*********************/
curses.endwin()

