# AsteroidsSPI - Raspberry Pi Asteroids Using SPI Display and SPI GPIO
# Copyright (C) 2015 Jason Birch
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
#/* AsteroidsSPI - Raspberry Pi Asteroids Using SPI Display and SPI GPIO     */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2016-11-03 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Conversion of Asteroids example game programming on multiple platforms,  */
#/* for Python on the Raspberry Pi using a 128x64 OLED SPI display and SPI   */
#/* GPIO port extender. The RPiSPiDev device driver is used to interface the */
#/* Python code with the SPI hardware.                                       */
#/****************************************************************************/


import struct
import Common


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



SPiDisplayFile = file



#  /***************************/
# /* Set the play area size. */
#/***************************/
class DesktopType:
   DISPLAY_X = 0
   DISPLAY_Y = 0
   DISPLAY_WIDTH = 128
   DISPLAY_HEIGHT = 64

   def __init__(self):
      self.x = self.DISPLAY_X
      self.y = self.DISPLAY_Y
      self.width = self.DISPLAY_WIDTH
      self.height = self.DISPLAY_HEIGHT


class XPoint:
   def __init__(self):
      self.x = 0
      self.y = 0


Desktop = DesktopType()



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



def DoDisplay(*Args):
   global SPiDisplayFile

   Message = ""
   for Count in range(len(Args)):
      if isinstance(Args[Count], str):
         Message += Args[Count]
      else:
         Message += struct.pack('I', Args[Count])
   SPiDisplayFile.write(Message)



def InitSPI():
   global SPiDisplayFile

   WriteGPIO("/dev/RPiSPi_011_001_4_3_MCP23S17_IODIR", 0xFFFF)
   WriteGPIO("/dev/RPiSPi_011_001_4_4_MCP23S17_IPOL", 0xF00F)
   WriteGPIO("/dev/RPiSPi_011_001_4_5_MCP23S17_GPINTEN", 0x0000)
   WriteGPIO("/dev/RPiSPi_011_001_4_6_MCP23S17_DEFVAL", 0x0000)
   WriteGPIO("/dev/RPiSPi_011_001_4_7_MCP23S17_INTCON", 0x0000)
   WriteGPIO("/dev/RPiSPi_011_001_4_8_MCP23S17_GPPU", 0xF00F)
   
   SPiDisplayFile = open("/dev/RPiSPi_010_000_2_1_SSD1306_WRITE", 'wb', 0)

   DoDisplay(SPI_DEV_CMD_SSD1306_ON)
   DoDisplay(SPI_DEV_CMD_SSD1306_CONTRAST, 127)
   DoDisplay(SPI_DEV_PRC_SSD1306_CLS)



def CloseSPI():
   global SPiDisplayFile

   DoDisplay(SPI_DEV_CMD_SSD1306_OFF)
   SPiDisplayFile.close()



def GetGpioKeys():
   return ReadGPIO("/dev/RPiSPi_011_001_4_2_MCP23S17_READ")



def DrawLine(X1, Y1, X2, Y2, Colour):
   if not (X1 < 0 and X2 < 0 or Y2 < 0 and Y2 < 0):
      if X1 < 0:
         X1 = 0
      if X2 < 0:
         X2 = 0
      if Y1 < 0:
         Y1 = 0
      if Y2 < 0:
         Y2 = 0
      DoDisplay(SPI_DEV_PRC_SSD1306_LINE, X1, Y1, X2, Y2, Colour)



def DrawLines(Points, PointCount, Colour):
   for Count in range(PointCount - 1):
      DrawLine(Points[Count].x, Points[Count].y, Points[Count + 1].x, Points[Count + 1].y, Colour)



def FillRectangle(X, Y, SizeX, SizeY, Colour):
   if X < 0:
      X = 0
   if Y < 0:
      Y = 0
   DoDisplay(SPI_DEV_PRC_SSD1306_BOX_FILL, X, Y, X + SizeX, Y + SizeY, Colour)



def DrawUpdate():
   DoDisplay(SPI_DEV_PRC_SSD1306_UPDATE)

