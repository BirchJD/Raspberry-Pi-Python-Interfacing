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


import random
import pygame
import Common


class AstroRock:
   SCALE = 0.25
   FRAMES = 3
   FRAME_POINTS = 9
   ROCK_WIDTH = 12
   ROCK_HEIGHT = 12
   ERASE = 3
   INACTIVE = 4
   NEW_POSITION = -1
   HYPERSPACE = -500


   def __init__(self):
      self.Scale = self.SCALE
      self.xMax = 0
      self.yMax = 0
      self.xOffset = self.HYPERSPACE
      self.yOffset = self.HYPERSPACE
      self.xVelocity = 0
      self.yVelocity = 0
      self.Frame = [[Common.XPoint() for X in range(self.FRAME_POINTS)] for Y in range(self.FRAMES)]
      self.DisplayFrame = [Common.XPoint() for X in range(self.FRAME_POINTS)]
      self.OldFrame = [Common.XPoint() for X in range(self.FRAME_POINTS)]

      self.RockWav = pygame.mixer.Sound("Sounds/Rock.wav")

      for self.Size in range(self.FRAMES):
         self.Frame[self.Size][0].x = self.Scale * -30 / (self.Size * self.Size + 1)
         self.Frame[self.Size][0].y = self.Scale * -22 / (self.Size * self.Size + 1)
         self.Frame[self.Size][1].x = self.Scale * -5 / (self.Size * self.Size + 1)
         self.Frame[self.Size][1].y = self.Scale * -32 / (self.Size * self.Size + 1)
         self.Frame[self.Size][2].x = self.Scale * +35 / (self.Size * self.Size + 1)
         self.Frame[self.Size][2].y = self.Scale * -17 / (self.Size * self.Size + 1)
         self.Frame[self.Size][3].x = self.Scale * +25 / (self.Size * self.Size + 1)
         self.Frame[self.Size][3].y = self.Scale * +28 / (self.Size * self.Size + 1)
         self.Frame[self.Size][4].x = self.Scale * +12 / (self.Size * self.Size + 1)
         self.Frame[self.Size][4].y = self.Scale * -2 / (self.Size * self.Size + 1)
         self.Frame[self.Size][5].x = self.Scale * +10 / (self.Size * self.Size + 1)
         self.Frame[self.Size][5].y = self.Scale * +28 / (self.Size * self.Size + 1)
         self.Frame[self.Size][6].x = self.Scale * -20 / (self.Size * self.Size + 1)
         self.Frame[self.Size][6].y = self.Scale * +33 / (self.Size * self.Size + 1)
         self.Frame[self.Size][7].x = self.Scale * -37 / (self.Size * self.Size + 1)
         self.Frame[self.Size][7].y = self.Scale * +5 / (self.Size * self.Size + 1)
         self.Frame[self.Size][8].x = self.Scale * -30 / (self.Size * self.Size + 1)
         self.Frame[self.Size][8].y = self.Scale * -22 / (self.Size * self.Size + 1)

      self.Size = self.INACTIVE



   def Draw(self):
      if self.Size < self.INACTIVE:
         Common.DrawLines(self.OldFrame, self.FRAME_POINTS, 0)

         if self.Size == self.ERASE:
            self.Size = self.INACTIVE

         if self.Size < self.INACTIVE:
            for self.Count in range(self.FRAME_POINTS):
               self.DisplayFrame[self.Count].x = self.Frame[self.Size][self.Count].x + self.xOffset
               self.DisplayFrame[self.Count].y = self.Frame[self.Size][self.Count].y + self.yOffset

            Common.DrawLines(self.DisplayFrame, self.FRAME_POINTS, 1)

            for self.Count in range(self.FRAME_POINTS):
               self.OldFrame[self.Count].x = self.DisplayFrame[self.Count].x
               self.OldFrame[self.Count].y = self.DisplayFrame[self.Count].y



   def Move(self):
      if self.Size < self.INACTIVE:
         if self.xOffset < 0 - self.ROCK_WIDTH:
            self.xOffset = self.xMax + self.ROCK_WIDTH
         elif self.xOffset > self.xMax + self.ROCK_WIDTH:
            self.xOffset = 0 - self.ROCK_WIDTH
         if self.yOffset < 0 - self.ROCK_HEIGHT:
            self.yOffset = self.yMax + self.ROCK_HEIGHT
         elif self.yOffset > self.yMax + self.ROCK_HEIGHT:
            self.yOffset = 0 - self.ROCK_HEIGHT
         self.xOffset += self.xVelocity
         self.yOffset += self.yVelocity



   def SetArea(self, Desktop, NewxOffset, NewyOffset, NewSize):
      self.xMax = Desktop.width - Desktop.x
      self.yMax = Desktop.height - Desktop.y
      if NewxOffset == self.NEW_POSITION:
         self.Size = 0
         if random.randrange(2) == False:
            self.xOffset = random.randrange(self.xMax)
            self.yOffset = self.yMax * random.randrange(2)
         else:
            self.yOffset = random.randrange(self.yMax)
            self.xOffset = self.xMax * random.randrange(2)
      else:
         self.Size = NewSize
         self.xOffset = NewxOffset
         self.yOffset = NewyOffset

      self.xVelocity = 0
      self.yVelocity = 0
      while self.xVelocity == 0 or self.yVelocity == 0:
         self.xVelocity = random.randrange(2 * (self.Size + 1)) - 1 * (self.Size + 1)
         self.yVelocity = random.randrange(2 * (self.Size + 1)) - 1 * (self.Size + 1)



   def Collide(self, xPos, yPos, Width, Height):
      self.Collision = False

      if self.Size < self.INACTIVE:
         self.Collision = xPos + Width / 2 > self.xOffset - self.ROCK_WIDTH / (self.Size * self.Size + 1) and xPos - Width / 2 < self.xOffset + self.ROCK_WIDTH / (self.Size * self.Size + 1) and yPos + Height / 2 > self.yOffset - self.ROCK_HEIGHT / (self.Size * self.Size + 1) and yPos - Height / 2 < self.yOffset + self.ROCK_HEIGHT / (self.Size * self.Size + 1)
         if self.Collision == True:
            self.RockWav.play()
            self.Size += 1

            self.xVelocity = 0
            self.yVelocity = 0
            while self.xVelocity == 0 or self.yVelocity == 0:
               self.xVelocity = random.randrange(6 * (self.Size + 1)) - 3 * (self.Size + 1)
               self.yVelocity = random.randrange(6 * (self.Size + 1)) - 3 * (self.Size + 1)

      return  self.Collision



   def Destroy(self):
      self.Size = self.ERASE
      self.xOffset = self.HYPERSPACE
      self.yOffset = self.HYPERSPACE



   def GetSize(self):
      return self.Size



   def GetXOffset(self):
      return self.xOffset



   def GetYOffset(self):
      return self.yOffset

