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


class AstroShot:
   SMALL_SHOT = 0
   LARGE_SHOT = 1
   SMALL_SHOT_FRAMES = 10
   LARGE_SHOT_FRAMES = 5
   ERASE_FRAME = 1
   HYPERSPACE = -500


   def __init__(self):
      self.xMax = 0
      self.yMax = 0
      self.xOffset = self.HYPERSPACE
      self.yOffset = self.HYPERSPACE
      self.OldxOffset = self.HYPERSPACE
      self.OldyOffset = self.HYPERSPACE
      self.xVelocity = 0
      self.yVelocity = 0
      self.Size = self.SMALL_SHOT
      self.FrameCount = 0



   def Draw(self):
      if self.FrameCount != False:
         if self.FrameCount == self.ERASE_FRAME:
            self.FrameCount = False

         if self.Size == self.SMALL_SHOT:
            Common.FillRectangle(self.OldxOffset, self.OldyOffset, 1, 1, 0)

            if self.FrameCount != False:
               Common.FillRectangle(self.xOffset, self.yOffset, 1, 1, 1)

               self.OldxOffset = self.xOffset
               self.OldyOffset = self.yOffset
         else:
            Common.FillRectangle(self.OldxOffset, self.OldyOffset, 2, 2, 0)

            if self.FrameCount != False:
               Common.FillRectangle(self.xOffset, self.yOffset, 2, 2, 1)

               self.OldxOffset = self.xOffset
               self.OldyOffset = self.yOffset



   def Move(self):
      if self.FrameCount > self.ERASE_FRAME:
         if self.xOffset < 0:
            self.xOffset = self.xMax
         elif self.xOffset > self.xMax:
            self.xOffset = 0
         if self.yOffset < 0:
            self.yOffset = self.yMax
         elif self.yOffset > self.yMax:
            self.yOffset = 0
         self.xOffset += self.xVelocity
         self.yOffset += self.yVelocity
         self.FrameCount -= 1



   def SetArea(self, NewxMax, NewyMax, NewxOffset, NewyOffset, NewxVelocity, NewyVelocity, NewSize):
      self.xMax = NewxMax
      self.yMax = NewyMax
      self.xOffset = NewxOffset
      self.yOffset = NewyOffset
      self.xVelocity = NewxVelocity
      self.yVelocity = NewyVelocity
      self.Size = NewSize
      if self.Size == self.LARGE_SHOT:
         self.FrameCount = self.LARGE_SHOT_FRAMES
      else:
         self.FrameCount = self.SMALL_SHOT_FRAMES



   def GetXOffset(self):
      return self.xOffset



   def GetYOffset(self):
      return self.yOffset



   def Destroy(self):
      self.FrameCount = self.ERASE_FRAME
      self.xOffset = self.HYPERSPACE
      self.yOffset = self.HYPERSPACE



   def Active(self):
      return (self.FrameCount != False)

