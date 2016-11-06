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


import Common


class Number:
   DIGITS = 10
   MAX_POINTS = 10


   def __init__(self):
      self.NumberValue = 0
      self.xOffset = 0
      self.yOffset = 0
      self.Scale = 0
      self.TextColour = 0

      self.Decimal = [[Common.XPoint() for X in range(self.MAX_POINTS + 1)] for Y in range(self.DIGITS)]
      self.DisplayFrame = [[Common.XPoint() for X in range(self.MAX_POINTS + 1)] for Y in range(self.DIGITS)]
      self.OldFrame = [[Common.XPoint() for X in range(self.MAX_POINTS + 1)] for Y in range(self.DIGITS)]



   def Draw(self):
#  /*****************************/
# /* Plot score current value. */
#/*****************************/
      self.TempValue = self.NumberValue
      for self.Digit in range(5):
         self.Divide = self.TempValue % 10
         for self.Count in range(self.Decimal[self.Divide][self.MAX_POINTS].x):
            self.DisplayFrame[self.Digit][self.Count].x = self.Decimal[self.Divide][self.Count].x + self.xOffset + (5 - self.Digit) * 3 * self.Scale
            self.DisplayFrame[self.Digit][self.Count].y = self.Decimal[self.Divide][self.Count].y + self.yOffset

         self.DisplayFrame[self.Digit][self.MAX_POINTS].x = self.Decimal[self.Divide][self.MAX_POINTS].x
         self.TempValue /= 10

#  /*************************/
# /* Erase previous score. */
#/*************************/
         Common.DrawLines(self.OldFrame[self.Digit], self.OldFrame[self.Digit][self.MAX_POINTS].x, 0)

#  /***************************/
# /* Draw the current score. */
#/***************************/
         Common.DrawLines(self.DisplayFrame[self.Digit], self.DisplayFrame[self.Digit][self.MAX_POINTS].x, 1)

#   /***************************************/
#  /* Plot current score,                 */
# /* next time it will be the old score. */
#/***************************************/
         for self.Count in range(self.DisplayFrame[self.Digit][self.MAX_POINTS].x):
            self.OldFrame[self.Digit][self.Count].x = self.DisplayFrame[self.Digit][self.Count].x
            self.OldFrame[self.Digit][self.Count].y = self.DisplayFrame[self.Digit][self.Count].y

         self.OldFrame[self.Digit][self.MAX_POINTS].x = self.DisplayFrame[self.Digit][self.MAX_POINTS].x



   def SetLocation(self, NewxOffset, NewyOffset, NewScale, NewTextColour):
      self.xOffset = NewxOffset
      self.yOffset = NewyOffset
      self.Scale = NewScale
      self.TextColour = NewTextColour

      self.Decimal[0][self.MAX_POINTS].x = 6
      self.Decimal[0][0].x = 2 * self.Scale
      self.Decimal[0][0].y = 0 * self.Scale
      self.Decimal[0][1].x = 0 * self.Scale
      self.Decimal[0][1].y = 0 * self.Scale
      self.Decimal[0][2].x = 0 * self.Scale
      self.Decimal[0][2].y = 4 * self.Scale
      self.Decimal[0][3].x = 2 * self.Scale
      self.Decimal[0][3].y = 4 * self.Scale
      self.Decimal[0][4].x = 2 * self.Scale
      self.Decimal[0][4].y = 0 * self.Scale
      self.Decimal[0][5].x = 0 * self.Scale
      self.Decimal[0][5].y = 4 * self.Scale

      self.Decimal[1][self.MAX_POINTS].x = 2
      self.Decimal[1][0].x = 1 * self.Scale
      self.Decimal[1][0].y = 0 * self.Scale
      self.Decimal[1][1].x = 1 * self.Scale
      self.Decimal[1][1].y = 4 * self.Scale

      self.Decimal[2][self.MAX_POINTS].x = 6
      self.Decimal[2][0].x = 0 * self.Scale
      self.Decimal[2][0].y = 0 * self.Scale
      self.Decimal[2][1].x = 2 * self.Scale
      self.Decimal[2][1].y = 0 * self.Scale
      self.Decimal[2][2].x = 2 * self.Scale
      self.Decimal[2][2].y = 2 * self.Scale
      self.Decimal[2][3].x = 0 * self.Scale
      self.Decimal[2][3].y = 2 * self.Scale
      self.Decimal[2][4].x = 0 * self.Scale
      self.Decimal[2][4].y = 4 * self.Scale
      self.Decimal[2][5].x = 2 * self.Scale
      self.Decimal[2][5].y = 4 * self.Scale

      self.Decimal[3][self.MAX_POINTS].x = 7
      self.Decimal[3][0].x = 0 * self.Scale
      self.Decimal[3][0].y = 0 * self.Scale
      self.Decimal[3][1].x = 2 * self.Scale
      self.Decimal[3][1].y = 0 * self.Scale
      self.Decimal[3][2].x = 2 * self.Scale
      self.Decimal[3][2].y = 2 * self.Scale
      self.Decimal[3][3].x = 0 * self.Scale
      self.Decimal[3][3].y = 2 * self.Scale
      self.Decimal[3][4].x = 2 * self.Scale
      self.Decimal[3][4].y = 2 * self.Scale
      self.Decimal[3][5].x = 2 * self.Scale
      self.Decimal[3][5].y = 4 * self.Scale
      self.Decimal[3][6].x = 0 * self.Scale
      self.Decimal[3][6].y = 4 * self.Scale

      self.Decimal[4][self.MAX_POINTS].x = 5
      self.Decimal[4][0].x = 0 * self.Scale
      self.Decimal[4][0].y = 0 * self.Scale
      self.Decimal[4][1].x = 0 * self.Scale
      self.Decimal[4][1].y = 2 * self.Scale
      self.Decimal[4][2].x = 2 * self.Scale
      self.Decimal[4][2].y = 2 * self.Scale
      self.Decimal[4][3].x = 2 * self.Scale
      self.Decimal[4][3].y = 0 * self.Scale
      self.Decimal[4][4].x = 2 * self.Scale
      self.Decimal[4][4].y = 4 * self.Scale

      self.Decimal[5][self.MAX_POINTS].x = 6
      self.Decimal[5][0].x = 2 * self.Scale
      self.Decimal[5][0].y = 0 * self.Scale
      self.Decimal[5][1].x = 0 * self.Scale
      self.Decimal[5][1].y = 0 * self.Scale
      self.Decimal[5][2].x = 0 * self.Scale
      self.Decimal[5][2].y = 2 * self.Scale
      self.Decimal[5][3].x = 2 * self.Scale
      self.Decimal[5][3].y = 2 * self.Scale
      self.Decimal[5][4].x = 2 * self.Scale
      self.Decimal[5][4].y = 4 * self.Scale
      self.Decimal[5][5].x = 0 * self.Scale
      self.Decimal[5][5].y = 4 * self.Scale

      self.Decimal[6][self.MAX_POINTS].x = 6
      self.Decimal[6][0].x = 2 * self.Scale
      self.Decimal[6][0].y = 0 * self.Scale
      self.Decimal[6][1].x = 0 * self.Scale
      self.Decimal[6][1].y = 0 * self.Scale
      self.Decimal[6][2].x = 0 * self.Scale
      self.Decimal[6][2].y = 4 * self.Scale
      self.Decimal[6][3].x = 2 * self.Scale
      self.Decimal[6][3].y = 4 * self.Scale
      self.Decimal[6][4].x = 2 * self.Scale
      self.Decimal[6][4].y = 2 * self.Scale
      self.Decimal[6][5].x = 0 * self.Scale
      self.Decimal[6][5].y = 2 * self.Scale

      self.Decimal[7][self.MAX_POINTS].x = 3
      self.Decimal[7][0].x = 0 * self.Scale
      self.Decimal[7][0].y = 0 * self.Scale
      self.Decimal[7][1].x = 2 * self.Scale
      self.Decimal[7][1].y = 0 * self.Scale
      self.Decimal[7][2].x = 2 * self.Scale
      self.Decimal[7][2].y = 4 * self.Scale

      self.Decimal[8][self.MAX_POINTS].x = 7
      self.Decimal[8][0].x = 0 * self.Scale
      self.Decimal[8][0].y = 0 * self.Scale
      self.Decimal[8][1].x = 2 * self.Scale
      self.Decimal[8][1].y = 0 * self.Scale
      self.Decimal[8][2].x = 2 * self.Scale
      self.Decimal[8][2].y = 4 * self.Scale
      self.Decimal[8][3].x = 0 * self.Scale
      self.Decimal[8][3].y = 4 * self.Scale
      self.Decimal[8][4].x = 0 * self.Scale
      self.Decimal[8][4].y = 0 * self.Scale
      self.Decimal[8][5].x = 0 * self.Scale
      self.Decimal[8][5].y = 2 * self.Scale
      self.Decimal[8][6].x = 2 * self.Scale
      self.Decimal[8][6].y = 2 * self.Scale

      self.Decimal[9][self.MAX_POINTS].x = 6
      self.Decimal[9][0].x = 0 * self.Scale
      self.Decimal[9][0].y = 4 * self.Scale
      self.Decimal[9][1].x = 2 * self.Scale
      self.Decimal[9][1].y = 4 * self.Scale
      self.Decimal[9][2].x = 2 * self.Scale
      self.Decimal[9][2].y = 0 * self.Scale
      self.Decimal[9][3].x = 0 * self.Scale
      self.Decimal[9][3].y = 0 * self.Scale
      self.Decimal[9][4].x = 0 * self.Scale
      self.Decimal[9][4].y = 2 * self.Scale
      self.Decimal[9][5].x = 2 * self.Scale
      self.Decimal[9][5].y = 2 * self.Scale



   def GetNumber(self):
      return self.NumberValue



   def SetNumber(self, NewNumber):
      self.NumberValue = NewNumber

