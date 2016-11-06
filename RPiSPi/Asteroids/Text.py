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


class Text:
   MAX_LETTERS = 58
   MAX_POINTS = 12
   MAX_TEXT = 2048
   INFINATE_FRAMES = -1


   def __init__(self):
      self.TextString = ""
      self.xOffset = 0
      self.yOffset = 0
      self.Scale = 0
      self.TextColour = 0
      self.Visible = False
      self.LastVisible = False
      self.FlashVisible = False
      self.Active = False
      self.Frames = self.INFINATE_FRAMES
      self.FrameCount = 0
      self.Flash = False

      self.Letter = [[Common.XPoint() for X in range(self.MAX_POINTS + 1)] for Y in range(self.MAX_LETTERS + 1)]
      self.DisplayFrame = [[Common.XPoint() for X in range(self.MAX_POINTS + 1)] for Y in range(self.MAX_TEXT + 1)]



   def Draw(self):
      if self.Active == True:
#  /********************************************/
# /* Display only for given number of frames. */
#/********************************************/
         if self.FrameCount != self.INFINATE_FRAMES:
            self.FrameCount -= 1
         if self.FrameCount == False and self.Flash == True:
            self.FrameCount = self.Frames
            self.FlashVisible = not self.FlashVisible
         elif self.FrameCount == False:
            self.Active = False

#  /****************************/
# /* Plot Text current value. */
#/****************************/
         for self.Digit in range(self.MAX_TEXT):
            if self.Digit >= len(self.TextString):
               break
            if self.TextString[self.Digit] >= '!' and self.TextString[self.Digit] <= 'Z':
#  /************************/
# /* Erase previous Text. */
#/************************/
               if self.Active == False or self.Visible == False or self.FlashVisible == False:
                  Common.DrawLines(self.DisplayFrame[self.Digit], self.DisplayFrame[self.Digit][self.MAX_POINTS].x, 0)
               else:
#  /**************************/
# /* Draw the current Text. */
#/**************************/
                  Common.DrawLines(self.DisplayFrame[self.Digit], self.DisplayFrame[self.Digit][self.MAX_POINTS].x, 1)



   def SetLocation(self, NewxOffset, NewyOffset, NewScale, NewFrames, NewFlash, NewText, NewTextColour):
      self.xOffsetOrig = NewxOffset
      self.xOffset = NewxOffset
      self.yOffset = NewyOffset
      self.Scale = NewScale
      self.TextColour = NewTextColour
      self.Frames = NewFrames
      self.Flash = NewFlash
      self.TextString = NewText
      self.Length = len(self.TextString)
      self.TextString = self.TextString.upper()

# !
      self.Letter[0][self.MAX_POINTS].x = 2
      self.Letter[0][0].x = 2 * self.Scale
      self.Letter[0][0].y = 0 * self.Scale
      self.Letter[0][1].x = 2 * self.Scale
      self.Letter[0][1].y = 3 * self.Scale
# "
      self.Letter[1][self.MAX_POINTS].x = 4
      self.Letter[1][0].x = 1 * self.Scale
      self.Letter[1][0].y = 1 * self.Scale
      self.Letter[1][1].x = 1 * self.Scale
      self.Letter[1][1].y = 0 * self.Scale
      self.Letter[1][2].x = 2 * self.Scale
      self.Letter[1][2].y = 0 * self.Scale
      self.Letter[1][3].x = 2 * self.Scale
      self.Letter[1][3].y = 1 * self.Scale
# #
      self.Letter[2][self.MAX_POINTS].x = 11
      self.Letter[2][0].x = 1 * self.Scale
      self.Letter[2][0].y = 0 * self.Scale
      self.Letter[2][1].x = 1 * self.Scale
      self.Letter[2][1].y = 4 * self.Scale
      self.Letter[2][2].x = 1 * self.Scale
      self.Letter[2][2].y = 3 * self.Scale
      self.Letter[2][3].x = 0 * self.Scale
      self.Letter[2][3].y = 3 * self.Scale
      self.Letter[2][4].x = 3 * self.Scale
      self.Letter[2][4].y = 3 * self.Scale
      self.Letter[2][5].x = 2 * self.Scale
      self.Letter[2][5].y = 3 * self.Scale
      self.Letter[2][6].x = 2 * self.Scale
      self.Letter[2][6].y = 4 * self.Scale
      self.Letter[2][7].x = 2 * self.Scale
      self.Letter[2][7].y = 0 * self.Scale
      self.Letter[2][8].x = 2 * self.Scale
      self.Letter[2][8].y = 1 * self.Scale
      self.Letter[2][9].x = 3 * self.Scale
      self.Letter[2][9].y = 1 * self.Scale
      self.Letter[2][10].x = 0 * self.Scale
      self.Letter[2][10].y = 1 * self.Scale
# $
      self.Letter[3][self.MAX_POINTS].x = 9
      self.Letter[3][0].x = 3 * self.Scale
      self.Letter[3][0].y = 1 * self.Scale
      self.Letter[3][1].x = 1 * self.Scale
      self.Letter[3][1].y = 1 * self.Scale
      self.Letter[3][2].x = 0 * self.Scale
      self.Letter[3][2].y = 2 * self.Scale
      self.Letter[3][3].x = 3 * self.Scale
      self.Letter[3][3].y = 2 * self.Scale
      self.Letter[3][4].x = 2 * self.Scale
      self.Letter[3][4].y = 3 * self.Scale
      self.Letter[3][5].x = 0 * self.Scale
      self.Letter[3][5].y = 3 * self.Scale
      self.Letter[3][6].x = 1 * self.Scale
      self.Letter[3][6].y = 3 * self.Scale
      self.Letter[3][7].x = 0 * self.Scale
      self.Letter[3][7].y = 4 * self.Scale
      self.Letter[3][8].x = 3 * self.Scale
      self.Letter[3][8].y = 0 * self.Scale
# %
      self.Letter[4][self.MAX_POINTS].x = 11
      self.Letter[4][0].x = 0 * self.Scale
      self.Letter[4][0].y = 0 * self.Scale
      self.Letter[4][1].x = 0 * self.Scale
      self.Letter[4][1].y = 1 * self.Scale
      self.Letter[4][2].x = 1 * self.Scale
      self.Letter[4][2].y = 1 * self.Scale
      self.Letter[4][3].x = 1 * self.Scale
      self.Letter[4][3].y = 0 * self.Scale
      self.Letter[4][4].x = 0 * self.Scale
      self.Letter[4][4].y = 0 * self.Scale
      self.Letter[4][5].x = 3 * self.Scale
      self.Letter[4][5].y = 0 * self.Scale
      self.Letter[4][6].x = 0 * self.Scale
      self.Letter[4][6].y = 4 * self.Scale
      self.Letter[4][7].x = 3 * self.Scale
      self.Letter[4][7].y = 4 * self.Scale
      self.Letter[4][8].x = 3 * self.Scale
      self.Letter[4][8].y = 3 * self.Scale
      self.Letter[4][9].x = 2 * self.Scale
      self.Letter[4][9].y = 3 * self.Scale
      self.Letter[4][10].x = 2 * self.Scale
      self.Letter[4][10].y = 4 * self.Scale
# &
      self.Letter[5][self.MAX_POINTS].x = 7
      self.Letter[5][0].x = 3 * self.Scale
      self.Letter[5][0].y = 4 * self.Scale
      self.Letter[5][1].x = 0 * self.Scale
      self.Letter[5][1].y = 1 * self.Scale
      self.Letter[5][2].x = 1 * self.Scale
      self.Letter[5][2].y = 0 * self.Scale
      self.Letter[5][3].x = 2 * self.Scale
      self.Letter[5][3].y = 1 * self.Scale
      self.Letter[5][4].x = 0 * self.Scale
      self.Letter[5][4].y = 3 * self.Scale
      self.Letter[5][5].x = 1 * self.Scale
      self.Letter[5][5].y = 4 * self.Scale
      self.Letter[5][6].x = 3 * self.Scale
      self.Letter[5][6].y = 2 * self.Scale
# '
      self.Letter[6][self.MAX_POINTS].x = 2
      self.Letter[6][0].x = 2 * self.Scale
      self.Letter[6][0].y = 0 * self.Scale
      self.Letter[6][1].x = 1 * self.Scale
      self.Letter[6][1].y = 1 * self.Scale
# (
      self.Letter[7][self.MAX_POINTS].x = 6
      self.Letter[7][0].x = 2 * self.Scale
      self.Letter[7][0].y = 0 * self.Scale
      self.Letter[7][1].x = 1 * self.Scale
      self.Letter[7][1].y = 0 * self.Scale
      self.Letter[7][2].x = 0 * self.Scale
      self.Letter[7][2].y = 1 * self.Scale
      self.Letter[7][3].x = 0 * self.Scale
      self.Letter[7][3].y = 3 * self.Scale
      self.Letter[7][4].x = 1 * self.Scale
      self.Letter[7][4].y = 4 * self.Scale
      self.Letter[7][5].x = 2 * self.Scale
      self.Letter[7][5].y = 4 * self.Scale
# )
      self.Letter[8][self.MAX_POINTS].x = 6
      self.Letter[8][0].x = 1 * self.Scale
      self.Letter[8][0].y = 0 * self.Scale
      self.Letter[8][1].x = 2 * self.Scale
      self.Letter[8][1].y = 0 * self.Scale
      self.Letter[8][2].x = 3 * self.Scale
      self.Letter[8][2].y = 1 * self.Scale
      self.Letter[8][3].x = 3 * self.Scale
      self.Letter[8][3].y = 3 * self.Scale
      self.Letter[8][4].x = 2 * self.Scale
      self.Letter[8][4].y = 4 * self.Scale
      self.Letter[8][5].x = 1 * self.Scale
      self.Letter[8][5].y = 4 * self.Scale
# *
      self.Letter[9][self.MAX_POINTS].x = 11
      self.Letter[9][0].x = 0 * self.Scale
      self.Letter[9][0].y = 1 * self.Scale
      self.Letter[9][1].x = 2 * self.Scale
      self.Letter[9][1].y = 3 * self.Scale
      self.Letter[9][2].x = 1 * self.Scale
      self.Letter[9][2].y = 2 * self.Scale
      self.Letter[9][3].x = 0 * self.Scale
      self.Letter[9][3].y = 3 * self.Scale
      self.Letter[9][4].x = 2 * self.Scale
      self.Letter[9][4].y = 1 * self.Scale
      self.Letter[9][5].x = 1 * self.Scale
      self.Letter[9][5].y = 2 * self.Scale
      self.Letter[9][6].x = 0 * self.Scale
      self.Letter[9][6].y = 2 * self.Scale
      self.Letter[9][7].x = 2 * self.Scale
      self.Letter[9][7].y = 2 * self.Scale
      self.Letter[9][8].x = 1 * self.Scale
      self.Letter[9][8].y = 2 * self.Scale
      self.Letter[9][9].x = 1 * self.Scale
      self.Letter[9][9].y = 1 * self.Scale
      self.Letter[9][10].x = 1 * self.Scale
      self.Letter[9][10].y = 3 * self.Scale
# +
      self.Letter[10][self.MAX_POINTS].x = 5
      self.Letter[10][0].x = 1 * self.Scale
      self.Letter[10][0].y = 1 * self.Scale
      self.Letter[10][1].x = 1 * self.Scale
      self.Letter[10][1].y = 3 * self.Scale
      self.Letter[10][2].x = 1 * self.Scale
      self.Letter[10][2].y = 2 * self.Scale
      self.Letter[10][3].x = 0 * self.Scale
      self.Letter[10][3].y = 2 * self.Scale
      self.Letter[10][4].x = 2 * self.Scale
      self.Letter[10][4].y = 2 * self.Scale
# ,
      self.Letter[11][self.MAX_POINTS].x = 2
      self.Letter[11][0].x = 2 * self.Scale
      self.Letter[11][0].y = 3 * self.Scale
      self.Letter[11][1].x = 1 * self.Scale
      self.Letter[11][1].y = 4 * self.Scale
# -
      self.Letter[12][self.MAX_POINTS].x = 2
      self.Letter[12][0].x = 0 * self.Scale
      self.Letter[12][0].y = 2 * self.Scale
      self.Letter[12][1].x = 2 * self.Scale
      self.Letter[12][1].y = 2 * self.Scale
# .
      self.Letter[13][self.MAX_POINTS].x = 2
      self.Letter[13][0].x = 2 * self.Scale
      self.Letter[13][0].y = 4 * self.Scale
      self.Letter[13][1].x = 2 * self.Scale
      self.Letter[13][1].y = 4 * self.Scale
# /
      self.Letter[14][self.MAX_POINTS].x = 2
      self.Letter[14][0].x = 0 * self.Scale
      self.Letter[14][0].y = 4 * self.Scale
      self.Letter[14][1].x = 3 * self.Scale
      self.Letter[14][1].y = 0 * self.Scale
# 0
      self.Letter[15][self.MAX_POINTS].x = 9
      self.Letter[15][0].x = 1 * self.Scale
      self.Letter[15][0].y = 0 * self.Scale
      self.Letter[15][1].x = 2 * self.Scale
      self.Letter[15][1].y = 0 * self.Scale
      self.Letter[15][2].x = 3 * self.Scale
      self.Letter[15][2].y = 1 * self.Scale
      self.Letter[15][3].x = 3 * self.Scale
      self.Letter[15][3].y = 3 * self.Scale
      self.Letter[15][4].x = 2 * self.Scale
      self.Letter[15][4].y = 4 * self.Scale
      self.Letter[15][5].x = 1 * self.Scale
      self.Letter[15][5].y = 4 * self.Scale
      self.Letter[15][6].x = 0 * self.Scale
      self.Letter[15][6].y = 3 * self.Scale
      self.Letter[15][7].x = 0 * self.Scale
      self.Letter[15][7].y = 1 * self.Scale
      self.Letter[15][8].x = 1 * self.Scale
      self.Letter[15][8].y = 0 * self.Scale
# 1
      self.Letter[16][self.MAX_POINTS].x = 2
      self.Letter[16][0].x = 2 * self.Scale
      self.Letter[16][0].y = 0 * self.Scale
      self.Letter[16][1].x = 2 * self.Scale
      self.Letter[16][1].y = 4 * self.Scale
# 2
      self.Letter[17][self.MAX_POINTS].x = 9
      self.Letter[17][0].x = 0 * self.Scale
      self.Letter[17][0].y = 1 * self.Scale
      self.Letter[17][1].x = 1 * self.Scale
      self.Letter[17][1].y = 0 * self.Scale
      self.Letter[17][2].x = 2 * self.Scale
      self.Letter[17][2].y = 0 * self.Scale
      self.Letter[17][3].x = 3 * self.Scale
      self.Letter[17][3].y = 1 * self.Scale
      self.Letter[17][4].x = 2 * self.Scale
      self.Letter[17][4].y = 2 * self.Scale
      self.Letter[17][5].x = 1 * self.Scale
      self.Letter[17][5].y = 2 * self.Scale
      self.Letter[17][6].x = 0 * self.Scale
      self.Letter[17][6].y = 3 * self.Scale
      self.Letter[17][7].x = 0 * self.Scale
      self.Letter[17][7].y = 4 * self.Scale
      self.Letter[17][8].x = 3 * self.Scale
      self.Letter[17][8].y = 4 * self.Scale
# 3
      self.Letter[18][self.MAX_POINTS].x = 9
      self.Letter[18][0].x = 0 * self.Scale
      self.Letter[18][0].y = 0 * self.Scale
      self.Letter[18][1].x = 2 * self.Scale
      self.Letter[18][1].y = 0 * self.Scale
      self.Letter[18][2].x = 3 * self.Scale
      self.Letter[18][2].y = 1 * self.Scale
      self.Letter[18][3].x = 2 * self.Scale
      self.Letter[18][3].y = 2 * self.Scale
      self.Letter[18][4].x = 1 * self.Scale
      self.Letter[18][4].y = 2 * self.Scale
      self.Letter[18][5].x = 2 * self.Scale
      self.Letter[18][5].y = 2 * self.Scale
      self.Letter[18][6].x = 3 * self.Scale
      self.Letter[18][6].y = 3 * self.Scale
      self.Letter[18][7].x = 2 * self.Scale
      self.Letter[18][7].y = 4 * self.Scale
      self.Letter[18][8].x = 0 * self.Scale
      self.Letter[18][8].y = 4 * self.Scale
# 4
      self.Letter[19][self.MAX_POINTS].x = 4
      self.Letter[19][0].x = 2 * self.Scale
      self.Letter[19][0].y = 4 * self.Scale
      self.Letter[19][1].x = 2 * self.Scale
      self.Letter[19][1].y = 0 * self.Scale
      self.Letter[19][2].x = 0 * self.Scale
      self.Letter[19][2].y = 3 * self.Scale
      self.Letter[19][3].x = 3 * self.Scale
      self.Letter[19][3].y = 3 * self.Scale
# 5
      self.Letter[20][self.MAX_POINTS].x = 7
      self.Letter[20][0].x = 3 * self.Scale
      self.Letter[20][0].y = 0 * self.Scale
      self.Letter[20][1].x = 0 * self.Scale
      self.Letter[20][1].y = 0 * self.Scale
      self.Letter[20][2].x = 0 * self.Scale
      self.Letter[20][2].y = 2 * self.Scale
      self.Letter[20][3].x = 2 * self.Scale
      self.Letter[20][3].y = 2 * self.Scale
      self.Letter[20][4].x = 3 * self.Scale
      self.Letter[20][4].y = 3 * self.Scale
      self.Letter[20][5].x = 2 * self.Scale
      self.Letter[20][5].y = 4 * self.Scale
      self.Letter[20][6].x = 0 * self.Scale
      self.Letter[20][6].y = 4 * self.Scale
# 6
      self.Letter[21][self.MAX_POINTS].x = 9
      self.Letter[21][0].x = 3 * self.Scale
      self.Letter[21][0].y = 0 * self.Scale
      self.Letter[21][1].x = 1 * self.Scale
      self.Letter[21][1].y = 0 * self.Scale
      self.Letter[21][2].x = 0 * self.Scale
      self.Letter[21][2].y = 1 * self.Scale
      self.Letter[21][3].x = 0 * self.Scale
      self.Letter[21][3].y = 3 * self.Scale
      self.Letter[21][4].x = 1 * self.Scale
      self.Letter[21][4].y = 4 * self.Scale
      self.Letter[21][5].x = 2 * self.Scale
      self.Letter[21][5].y = 4 * self.Scale
      self.Letter[21][6].x = 3 * self.Scale
      self.Letter[21][6].y = 3 * self.Scale
      self.Letter[21][7].x = 3 * self.Scale
      self.Letter[21][7].y = 2 * self.Scale
      self.Letter[21][8].x = 0 * self.Scale
      self.Letter[21][8].y = 2 * self.Scale
# 7
      self.Letter[22][self.MAX_POINTS].x = 3
      self.Letter[22][0].x = 0 * self.Scale
      self.Letter[22][0].y = 0 * self.Scale
      self.Letter[22][1].x = 3 * self.Scale
      self.Letter[22][1].y = 0 * self.Scale
      self.Letter[22][2].x = 0 * self.Scale
      self.Letter[22][2].y = 4 * self.Scale
# 8
      self.Letter[23][self.MAX_POINTS].x = 9
      self.Letter[23][0].x = 0 * self.Scale
      self.Letter[23][0].y = 1 * self.Scale
      self.Letter[23][1].x = 1 * self.Scale
      self.Letter[23][1].y = 0 * self.Scale
      self.Letter[23][2].x = 2 * self.Scale
      self.Letter[23][2].y = 0 * self.Scale
      self.Letter[23][3].x = 3 * self.Scale
      self.Letter[23][3].y = 1 * self.Scale
      self.Letter[23][4].x = 0 * self.Scale
      self.Letter[23][4].y = 3 * self.Scale
      self.Letter[23][5].x = 1 * self.Scale
      self.Letter[23][5].y = 4 * self.Scale
      self.Letter[23][6].x = 2 * self.Scale
      self.Letter[23][6].y = 4 * self.Scale
      self.Letter[23][7].x = 3 * self.Scale
      self.Letter[23][7].y = 3 * self.Scale
      self.Letter[23][8].x = 0 * self.Scale
      self.Letter[23][8].y = 1 * self.Scale
# 9
      self.Letter[24][self.MAX_POINTS].x = 9
      self.Letter[24][0].x = 0 * self.Scale
      self.Letter[24][0].y = 4 * self.Scale
      self.Letter[24][1].x = 2 * self.Scale
      self.Letter[24][1].y = 4 * self.Scale
      self.Letter[24][2].x = 3 * self.Scale
      self.Letter[24][2].y = 3 * self.Scale
      self.Letter[24][3].x = 3 * self.Scale
      self.Letter[24][3].y = 1 * self.Scale
      self.Letter[24][4].x = 2 * self.Scale
      self.Letter[24][4].y = 0 * self.Scale
      self.Letter[24][5].x = 1 * self.Scale
      self.Letter[24][5].y = 0 * self.Scale
      self.Letter[24][6].x = 0 * self.Scale
      self.Letter[24][6].y = 1 * self.Scale
      self.Letter[24][7].x = 0 * self.Scale
      self.Letter[24][7].y = 2 * self.Scale
      self.Letter[24][8].x = 3 * self.Scale
      self.Letter[24][8].y = 2 * self.Scale
# :
      self.Letter[25][self.MAX_POINTS].x = 2
      self.Letter[25][0].x = 2 * self.Scale
      self.Letter[25][0].y = 1 * self.Scale
      self.Letter[25][1].x = 2 * self.Scale
      self.Letter[25][1].y = 3 * self.Scale
# ;
      self.Letter[26][self.MAX_POINTS].x = 3
      self.Letter[26][0].x = 2 * self.Scale
      self.Letter[26][0].y = 1 * self.Scale
      self.Letter[26][1].x = 2 * self.Scale
      self.Letter[26][1].y = 3 * self.Scale
      self.Letter[26][2].x = 1 * self.Scale
      self.Letter[26][2].y = 4 * self.Scale
# <
      self.Letter[27][self.MAX_POINTS].x = 3
      self.Letter[27][0].x = 3 * self.Scale
      self.Letter[27][0].y = 1 * self.Scale
      self.Letter[27][1].x = 0 * self.Scale
      self.Letter[27][1].y = 2 * self.Scale
      self.Letter[27][2].x = 3 * self.Scale
      self.Letter[27][2].y = 3 * self.Scale
# =
      self.Letter[28][self.MAX_POINTS].x = 4
      self.Letter[28][0].x = 3 * self.Scale
      self.Letter[28][0].y = 1 * self.Scale
      self.Letter[28][1].x = 0 * self.Scale
      self.Letter[28][1].y = 1 * self.Scale
      self.Letter[28][2].x = 0 * self.Scale
      self.Letter[28][2].y = 3 * self.Scale
      self.Letter[28][3].x = 3 * self.Scale
      self.Letter[28][3].y = 3 * self.Scale
# >
      self.Letter[29][self.MAX_POINTS].x = 3
      self.Letter[29][0].x = 0 * self.Scale
      self.Letter[29][0].y = 1 * self.Scale
      self.Letter[29][1].x = 3 * self.Scale
      self.Letter[29][1].y = 2 * self.Scale
      self.Letter[29][2].x = 0 * self.Scale
      self.Letter[29][2].y = 3 * self.Scale
# ?
      self.Letter[30][self.MAX_POINTS].x = 7
      self.Letter[30][0].x = 0 * self.Scale
      self.Letter[30][0].y = 1 * self.Scale
      self.Letter[30][1].x = 1 * self.Scale
      self.Letter[30][1].y = 0 * self.Scale
      self.Letter[30][2].x = 2 * self.Scale
      self.Letter[30][2].y = 0 * self.Scale
      self.Letter[30][3].x = 3 * self.Scale
      self.Letter[30][3].y = 1 * self.Scale
      self.Letter[30][4].x = 3 * self.Scale
      self.Letter[30][4].y = 2 * self.Scale
      self.Letter[30][5].x = 2 * self.Scale
      self.Letter[30][5].y = 3 * self.Scale
      self.Letter[30][6].x = 2 * self.Scale
      self.Letter[30][6].y = 4 * self.Scale
# @
      self.Letter[31][self.MAX_POINTS].x = 12
      self.Letter[31][0].x = 3 * self.Scale
      self.Letter[31][0].y = 4 * self.Scale
      self.Letter[31][1].x = 1 * self.Scale
      self.Letter[31][1].y = 4 * self.Scale
      self.Letter[31][2].x = 0 * self.Scale
      self.Letter[31][2].y = 3 * self.Scale
      self.Letter[31][3].x = 0 * self.Scale
      self.Letter[31][3].y = 1 * self.Scale
      self.Letter[31][4].x = 1 * self.Scale
      self.Letter[31][4].y = 0 * self.Scale
      self.Letter[31][5].x = 2 * self.Scale
      self.Letter[31][5].y = 0 * self.Scale
      self.Letter[31][6].x = 3 * self.Scale
      self.Letter[31][6].y = 1 * self.Scale
      self.Letter[31][7].x = 3 * self.Scale
      self.Letter[31][7].y = 2 * self.Scale
      self.Letter[31][8].x = 2 * self.Scale
      self.Letter[31][8].y = 3 * self.Scale
      self.Letter[31][9].x = 1 * self.Scale
      self.Letter[31][9].y = 2 * self.Scale
      self.Letter[31][10].x = 2 * self.Scale
      self.Letter[31][10].y = 1 * self.Scale
      self.Letter[31][11].x = 3 * self.Scale
      self.Letter[31][11].y = 1 * self.Scale
# A
      self.Letter[32][self.MAX_POINTS].x = 6
      self.Letter[32][0].x = 0 * self.Scale
      self.Letter[32][0].y = 4 * self.Scale
      self.Letter[32][1].x = 0 * self.Scale
      self.Letter[32][1].y = 0 * self.Scale
      self.Letter[32][2].x = 3 * self.Scale
      self.Letter[32][2].y = 0 * self.Scale
      self.Letter[32][3].x = 3 * self.Scale
      self.Letter[32][3].y = 4 * self.Scale
      self.Letter[32][4].x = 3 * self.Scale
      self.Letter[32][4].y = 2 * self.Scale
      self.Letter[32][5].x = 0 * self.Scale
      self.Letter[32][5].y = 2 * self.Scale
# B
      self.Letter[33][self.MAX_POINTS].x = 8
      self.Letter[33][0].x = 0 * self.Scale
      self.Letter[33][0].y = 0 * self.Scale
      self.Letter[33][1].x = 0 * self.Scale
      self.Letter[33][1].y = 4 * self.Scale
      self.Letter[33][2].x = 3 * self.Scale
      self.Letter[33][2].y = 4 * self.Scale
      self.Letter[33][3].x = 3 * self.Scale
      self.Letter[33][3].y = 3 * self.Scale
      self.Letter[33][4].x = 0 * self.Scale
      self.Letter[33][4].y = 2 * self.Scale
      self.Letter[33][5].x = 3 * self.Scale
      self.Letter[33][5].y = 1 * self.Scale
      self.Letter[33][6].x = 3 * self.Scale
      self.Letter[33][6].y = 0 * self.Scale
      self.Letter[33][7].x = 0 * self.Scale
      self.Letter[33][7].y = 0 * self.Scale
# C
      self.Letter[34][self.MAX_POINTS].x = 6
      self.Letter[34][0].x = 3 * self.Scale
      self.Letter[34][0].y = 0 * self.Scale
      self.Letter[34][1].x = 1 * self.Scale
      self.Letter[34][1].y = 0 * self.Scale
      self.Letter[34][2].x = 0 * self.Scale
      self.Letter[34][2].y = 1 * self.Scale
      self.Letter[34][3].x = 0 * self.Scale
      self.Letter[34][3].y = 3 * self.Scale
      self.Letter[34][4].x = 1 * self.Scale
      self.Letter[34][4].y = 4 * self.Scale
      self.Letter[34][5].x = 3 * self.Scale
      self.Letter[34][5].y = 4 * self.Scale
# D
      self.Letter[35][self.MAX_POINTS].x = 6
      self.Letter[35][0].x = 0 * self.Scale
      self.Letter[35][0].y = 0 * self.Scale
      self.Letter[35][1].x = 0 * self.Scale
      self.Letter[35][1].y = 4 * self.Scale
      self.Letter[35][2].x = 1 * self.Scale
      self.Letter[35][2].y = 4 * self.Scale
      self.Letter[35][3].x = 3 * self.Scale
      self.Letter[35][3].y = 2 * self.Scale
      self.Letter[35][4].x = 1 * self.Scale
      self.Letter[35][4].y = 0 * self.Scale
      self.Letter[35][5].x = 0 * self.Scale
      self.Letter[35][5].y = 0 * self.Scale
# E
      self.Letter[36][self.MAX_POINTS].x = 7
      self.Letter[36][0].x = 3 * self.Scale
      self.Letter[36][0].y = 0 * self.Scale
      self.Letter[36][1].x = 0 * self.Scale
      self.Letter[36][1].y = 0 * self.Scale
      self.Letter[36][2].x = 0 * self.Scale
      self.Letter[36][2].y = 2 * self.Scale
      self.Letter[36][3].x = 2 * self.Scale
      self.Letter[36][3].y = 2 * self.Scale
      self.Letter[36][4].x = 0 * self.Scale
      self.Letter[36][4].y = 2 * self.Scale
      self.Letter[36][5].x = 0 * self.Scale
      self.Letter[36][5].y = 4 * self.Scale
      self.Letter[36][6].x = 3 * self.Scale
      self.Letter[36][6].y = 4 * self.Scale
# F
      self.Letter[37][self.MAX_POINTS].x = 6
      self.Letter[37][0].x = 3 * self.Scale
      self.Letter[37][0].y = 0 * self.Scale
      self.Letter[37][1].x = 0 * self.Scale
      self.Letter[37][1].y = 0 * self.Scale
      self.Letter[37][2].x = 0 * self.Scale
      self.Letter[37][2].y = 2 * self.Scale
      self.Letter[37][3].x = 2 * self.Scale
      self.Letter[37][3].y = 2 * self.Scale
      self.Letter[37][4].x = 0 * self.Scale
      self.Letter[37][4].y = 2 * self.Scale
      self.Letter[37][5].x = 0 * self.Scale
      self.Letter[37][5].y = 4 * self.Scale
# G
      self.Letter[38][self.MAX_POINTS].x = 6
      self.Letter[38][0].x = 3 * self.Scale
      self.Letter[38][0].y = 0 * self.Scale
      self.Letter[38][1].x = 0 * self.Scale
      self.Letter[38][1].y = 0 * self.Scale
      self.Letter[38][2].x = 0 * self.Scale
      self.Letter[38][2].y = 4 * self.Scale
      self.Letter[38][3].x = 3 * self.Scale
      self.Letter[38][3].y = 4 * self.Scale
      self.Letter[38][4].x = 3 * self.Scale
      self.Letter[38][4].y = 2 * self.Scale
      self.Letter[38][5].x = 1 * self.Scale
      self.Letter[38][5].y = 2 * self.Scale
# H
      self.Letter[39][self.MAX_POINTS].x = 6
      self.Letter[39][0].x = 0 * self.Scale
      self.Letter[39][0].y = 0 * self.Scale
      self.Letter[39][1].x = 0 * self.Scale
      self.Letter[39][1].y = 4 * self.Scale
      self.Letter[39][2].x = 0 * self.Scale
      self.Letter[39][2].y = 2 * self.Scale
      self.Letter[39][3].x = 3 * self.Scale
      self.Letter[39][3].y = 2 * self.Scale
      self.Letter[39][4].x = 3 * self.Scale
      self.Letter[39][4].y = 0 * self.Scale
      self.Letter[39][5].x = 3 * self.Scale
      self.Letter[39][5].y = 4 * self.Scale
# I
      self.Letter[40][self.MAX_POINTS].x = 6
      self.Letter[40][0].x = 1 * self.Scale
      self.Letter[40][0].y = 0 * self.Scale
      self.Letter[40][1].x = 3 * self.Scale
      self.Letter[40][1].y = 0 * self.Scale
      self.Letter[40][2].x = 2 * self.Scale
      self.Letter[40][2].y = 0 * self.Scale
      self.Letter[40][3].x = 2 * self.Scale
      self.Letter[40][3].y = 4 * self.Scale
      self.Letter[40][4].x = 1 * self.Scale
      self.Letter[40][4].y = 4 * self.Scale
      self.Letter[40][5].x = 3 * self.Scale
      self.Letter[40][5].y = 4 * self.Scale
# J
      self.Letter[41][self.MAX_POINTS].x = 6
      self.Letter[41][0].x = 1 * self.Scale
      self.Letter[41][0].y = 0 * self.Scale
      self.Letter[41][1].x = 3 * self.Scale
      self.Letter[41][1].y = 0 * self.Scale
      self.Letter[41][2].x = 2 * self.Scale
      self.Letter[41][2].y = 0 * self.Scale
      self.Letter[41][3].x = 2 * self.Scale
      self.Letter[41][3].y = 4 * self.Scale
      self.Letter[41][4].x = 0 * self.Scale
      self.Letter[41][4].y = 4 * self.Scale
      self.Letter[41][5].x = 0 * self.Scale
      self.Letter[41][5].y = 3 * self.Scale
# K
      self.Letter[42][self.MAX_POINTS].x = 6
      self.Letter[42][0].x = 0 * self.Scale
      self.Letter[42][0].y = 0 * self.Scale
      self.Letter[42][1].x = 0 * self.Scale
      self.Letter[42][1].y = 4 * self.Scale
      self.Letter[42][2].x = 0 * self.Scale
      self.Letter[42][2].y = 2 * self.Scale
      self.Letter[42][3].x = 3 * self.Scale
      self.Letter[42][3].y = 0 * self.Scale
      self.Letter[42][4].x = 0 * self.Scale
      self.Letter[42][4].y = 2 * self.Scale
      self.Letter[42][5].x = 3 * self.Scale
      self.Letter[42][5].y = 4 * self.Scale
# L
      self.Letter[43][self.MAX_POINTS].x = 3
      self.Letter[43][0].x = 0 * self.Scale
      self.Letter[43][0].y = 0 * self.Scale
      self.Letter[43][1].x = 0 * self.Scale
      self.Letter[43][1].y = 4 * self.Scale
      self.Letter[43][2].x = 3 * self.Scale
      self.Letter[43][2].y = 4 * self.Scale
# M
      self.Letter[44][self.MAX_POINTS].x = 6
      self.Letter[44][0].x = 0 * self.Scale
      self.Letter[44][0].y = 4 * self.Scale
      self.Letter[44][1].x = 0 * self.Scale
      self.Letter[44][1].y = 0 * self.Scale
      self.Letter[44][2].x = 1 * self.Scale
      self.Letter[44][2].y = 2 * self.Scale
      self.Letter[44][3].x = 2 * self.Scale
      self.Letter[44][3].y = 2 * self.Scale
      self.Letter[44][4].x = 3 * self.Scale
      self.Letter[44][4].y = 0 * self.Scale
      self.Letter[44][5].x = 3 * self.Scale
      self.Letter[44][5].y = 4 * self.Scale
# N
      self.Letter[45][self.MAX_POINTS].x = 4
      self.Letter[45][0].x = 0 * self.Scale
      self.Letter[45][0].y = 4 * self.Scale
      self.Letter[45][1].x = 0 * self.Scale
      self.Letter[45][1].y = 0 * self.Scale
      self.Letter[45][2].x = 3 * self.Scale
      self.Letter[45][2].y = 4 * self.Scale
      self.Letter[45][3].x = 3 * self.Scale
      self.Letter[45][3].y = 0 * self.Scale
# O
      self.Letter[46][self.MAX_POINTS].x = 9
      self.Letter[46][0].x = 0 * self.Scale
      self.Letter[46][0].y = 1 * self.Scale
      self.Letter[46][1].x = 0 * self.Scale
      self.Letter[46][1].y = 3 * self.Scale
      self.Letter[46][2].x = 1 * self.Scale
      self.Letter[46][2].y = 4 * self.Scale
      self.Letter[46][3].x = 2 * self.Scale
      self.Letter[46][3].y = 4 * self.Scale
      self.Letter[46][4].x = 3 * self.Scale
      self.Letter[46][4].y = 3 * self.Scale
      self.Letter[46][5].x = 3 * self.Scale
      self.Letter[46][5].y = 1 * self.Scale
      self.Letter[46][6].x = 2 * self.Scale
      self.Letter[46][6].y = 0 * self.Scale
      self.Letter[46][7].x = 1 * self.Scale
      self.Letter[46][7].y = 0 * self.Scale
      self.Letter[46][8].x = 0 * self.Scale
      self.Letter[46][8].y = 1 * self.Scale
# P
      self.Letter[47][self.MAX_POINTS].x = 5
      self.Letter[47][0].x = 0 * self.Scale
      self.Letter[47][0].y = 4 * self.Scale
      self.Letter[47][1].x = 0 * self.Scale
      self.Letter[47][1].y = 0 * self.Scale
      self.Letter[47][2].x = 3 * self.Scale
      self.Letter[47][2].y = 0 * self.Scale
      self.Letter[47][3].x = 3 * self.Scale
      self.Letter[47][3].y = 2 * self.Scale
      self.Letter[47][4].x = 0 * self.Scale
      self.Letter[47][4].y = 2 * self.Scale
# Q
      self.Letter[48][self.MAX_POINTS].x = 6
      self.Letter[48][0].x = 2 * self.Scale
      self.Letter[48][0].y = 3 * self.Scale
      self.Letter[48][1].x = 3 * self.Scale
      self.Letter[48][1].y = 4 * self.Scale
      self.Letter[48][2].x = 0 * self.Scale
      self.Letter[48][2].y = 4 * self.Scale
      self.Letter[48][3].x = 0 * self.Scale
      self.Letter[48][3].y = 0 * self.Scale
      self.Letter[48][4].x = 3 * self.Scale
      self.Letter[48][4].y = 0 * self.Scale
      self.Letter[48][5].x = 3 * self.Scale
      self.Letter[48][5].y = 4 * self.Scale
# R
      self.Letter[49][self.MAX_POINTS].x = 6
      self.Letter[49][0].x = 0 * self.Scale
      self.Letter[49][0].y = 4 * self.Scale
      self.Letter[49][1].x = 0 * self.Scale
      self.Letter[49][1].y = 0 * self.Scale
      self.Letter[49][2].x = 3 * self.Scale
      self.Letter[49][2].y = 0 * self.Scale
      self.Letter[49][3].x = 3 * self.Scale
      self.Letter[49][3].y = 2 * self.Scale
      self.Letter[49][4].x = 0 * self.Scale
      self.Letter[49][4].y = 2 * self.Scale
      self.Letter[49][5].x = 3 * self.Scale
      self.Letter[49][5].y = 4 * self.Scale
# S
      self.Letter[50][self.MAX_POINTS].x = 8
      self.Letter[50][0].x = 3 * self.Scale
      self.Letter[50][0].y = 0 * self.Scale
      self.Letter[50][1].x = 1 * self.Scale
      self.Letter[50][1].y = 0 * self.Scale
      self.Letter[50][2].x = 0 * self.Scale
      self.Letter[50][2].y = 1 * self.Scale
      self.Letter[50][3].x = 1 * self.Scale
      self.Letter[50][3].y = 2 * self.Scale
      self.Letter[50][4].x = 2 * self.Scale
      self.Letter[50][4].y = 2 * self.Scale
      self.Letter[50][5].x = 3 * self.Scale
      self.Letter[50][5].y = 3 * self.Scale
      self.Letter[50][6].x = 2 * self.Scale
      self.Letter[50][6].y = 4 * self.Scale
      self.Letter[50][7].x = 0 * self.Scale
      self.Letter[50][7].y = 4 * self.Scale
# T
      self.Letter[51][self.MAX_POINTS].x = 4
      self.Letter[51][0].x = 1 * self.Scale
      self.Letter[51][0].y = 0 * self.Scale
      self.Letter[51][1].x = 3 * self.Scale
      self.Letter[51][1].y = 0 * self.Scale
      self.Letter[51][2].x = 2 * self.Scale
      self.Letter[51][2].y = 0 * self.Scale
      self.Letter[51][3].x = 2 * self.Scale
      self.Letter[51][3].y = 4 * self.Scale
# U
      self.Letter[52][self.MAX_POINTS].x = 6
      self.Letter[52][0].x = 0 * self.Scale
      self.Letter[52][0].y = 0 * self.Scale
      self.Letter[52][1].x = 0 * self.Scale
      self.Letter[52][1].y = 3 * self.Scale
      self.Letter[52][2].x = 1 * self.Scale
      self.Letter[52][2].y = 4 * self.Scale
      self.Letter[52][3].x = 2 * self.Scale
      self.Letter[52][3].y = 4 * self.Scale
      self.Letter[52][4].x = 3 * self.Scale
      self.Letter[52][4].y = 3 * self.Scale
      self.Letter[52][5].x = 3 * self.Scale
      self.Letter[52][5].y = 0 * self.Scale
# V
      self.Letter[53][self.MAX_POINTS].x = 4
      self.Letter[53][0].x = 0 * self.Scale
      self.Letter[53][0].y = 0 * self.Scale
      self.Letter[53][1].x = 1 * self.Scale
      self.Letter[53][1].y = 4 * self.Scale
      self.Letter[53][2].x = 2 * self.Scale
      self.Letter[53][2].y = 4 * self.Scale
      self.Letter[53][3].x = 3 * self.Scale
      self.Letter[53][3].y = 0 * self.Scale
# W
      self.Letter[54][self.MAX_POINTS].x = 6
      self.Letter[54][0].x = 0 * self.Scale
      self.Letter[54][0].y = 0 * self.Scale
      self.Letter[54][1].x = 0 * self.Scale
      self.Letter[54][1].y = 4 * self.Scale
      self.Letter[54][2].x = 1 * self.Scale
      self.Letter[54][2].y = 3 * self.Scale
      self.Letter[54][3].x = 2 * self.Scale
      self.Letter[54][3].y = 3 * self.Scale
      self.Letter[54][4].x = 3 * self.Scale
      self.Letter[54][4].y = 4 * self.Scale
      self.Letter[54][5].x = 3 * self.Scale
      self.Letter[54][5].y = 0 * self.Scale
# X
      self.Letter[55][self.MAX_POINTS].x = 7
      self.Letter[55][0].x = 1 * self.Scale
      self.Letter[55][0].y = 0 * self.Scale
      self.Letter[55][1].x = 2 * self.Scale
      self.Letter[55][1].y = 2 * self.Scale
      self.Letter[55][2].x = 3 * self.Scale
      self.Letter[55][2].y = 0 * self.Scale
      self.Letter[55][3].x = 2 * self.Scale
      self.Letter[55][3].y = 2 * self.Scale
      self.Letter[55][4].x = 1 * self.Scale
      self.Letter[55][4].y = 4 * self.Scale
      self.Letter[55][5].x = 2 * self.Scale
      self.Letter[55][5].y = 2 * self.Scale
      self.Letter[55][6].x = 3 * self.Scale
      self.Letter[55][6].y = 4 * self.Scale
# Y
      self.Letter[56][self.MAX_POINTS].x = 5
      self.Letter[56][0].x = 1 * self.Scale
      self.Letter[56][0].y = 0 * self.Scale
      self.Letter[56][1].x = 2 * self.Scale
      self.Letter[56][1].y = 2 * self.Scale
      self.Letter[56][2].x = 3 * self.Scale
      self.Letter[56][2].y = 0 * self.Scale
      self.Letter[56][3].x = 2 * self.Scale
      self.Letter[56][3].y = 2 * self.Scale
      self.Letter[56][4].x = 2 * self.Scale
      self.Letter[56][4].y = 4 * self.Scale
# Z
      self.Letter[57][self.MAX_POINTS].x = 4
      self.Letter[57][0].x = 0 * self.Scale
      self.Letter[57][0].y = 0 * self.Scale
      self.Letter[57][1].x = 3 * self.Scale
      self.Letter[57][1].y = 0 * self.Scale
      self.Letter[57][2].x = 0 * self.Scale
      self.Letter[57][2].y = 4 * self.Scale
      self.Letter[57][3].x = 3 * self.Scale
      self.Letter[57][3].y = 4 * self.Scale

      for self.Digit in range(self.MAX_TEXT):
         if self.Digit >= len(self.TextString):
            break
         if self.TextString[self.Digit] == '\n':
            self.xOffset = self.xOffsetOrig
            self.yOffset += 5 * self.Scale + 2
         elif self.TextString[self.Digit] >= '!' and self.TextString[self.Digit] <= 'Z':
            for self.Count in range(self.Letter[ord(self.TextString[self.Digit]) - ord('!')][self.MAX_POINTS].x):
               self.DisplayFrame[self.Digit][self.Count].x = self.Letter[ord(self.TextString[self.Digit]) - ord('!')][self.Count].x + self.xOffset
               self.DisplayFrame[self.Digit][self.Count].y = self.Letter[ord(self.TextString[self.Digit]) - ord('!')][self.Count].y + self.yOffset
            self.DisplayFrame[self.Digit][self.MAX_POINTS].x = self.Letter[ord(self.TextString[self.Digit]) - ord('!')][self.MAX_POINTS].x
            self.xOffset += 4 * self.Scale
         else:
            self.xOffset += 4 * self.Scale



   def SetVisible(self, NewVisible):
      if NewVisible != self.LastVisible:
         self.Visible = NewVisible
         self.LastVisible = self.Visible
         self.FlashVisible = self.Visible
         self.Active = True
         self.FrameCount = self.Frames



   def GetVisible(self):
      return self.Active

