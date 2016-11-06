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


import pygame
import random
import Common
import AstroShot


class AstroUFO:
   SCALE = 0.25
   FRAMES = 2
   FRAME_POINTS = 12
   UFO_WIDTH = 16
   UFO_HEIGHT = 6
   INACTIVE = 3
   ERASE = 4
   HYPERSPACE = -500


   def __init__(self):
      self.Scale = self.SCALE
      self.xMax = 0
      self.yMax = 0
      self.xOffset = self.HYPERSPACE
      self.yOffset = self.HYPERSPACE
      self.xVelocity = 0
      self.yVelocity = 0

      self.Shot = AstroShot.AstroShot()
      self.Frame = [[Common.XPoint() for X in range(self.FRAME_POINTS)] for Y in range(self.FRAMES)]
      self.DisplayFrame = [Common.XPoint() for X in range(self.FRAME_POINTS)]
      self.OldFrame = [Common.XPoint() for X in range(self.FRAME_POINTS)]

      self.UFOWav = pygame.mixer.Sound("Sounds/UFO.wav")
      self.UFOShotWav = pygame.mixer.Sound("Sounds/UFOShot.wav")

      for self.Size in range(self.FRAMES):
         self.Frame[self.Size][0].x = self.Scale * -(8 + (self.Size + 1) * 3)
         self.Frame[self.Size][0].y = self.Scale * -(0 + (self.Size + 1))
         self.Frame[self.Size][1].x = self.Scale * -(0 + (self.Size + 1))
         self.Frame[self.Size][1].y = self.Scale * -(3 + (self.Size + 1) * 3)
         self.Frame[self.Size][2].x = self.Scale * +(0 + (self.Size + 1))
         self.Frame[self.Size][2].y = self.Scale * -(3 + (self.Size + 1) * 3)
         self.Frame[self.Size][3].x = self.Scale * +(8 + (self.Size + 1) * 3)
         self.Frame[self.Size][3].y = self.Scale * -(0 + (self.Size + 1))
         self.Frame[self.Size][4].x = self.Scale * -(8 + (self.Size + 1) * 3)
         self.Frame[self.Size][4].y = self.Scale * -(0 + (self.Size + 1))
         self.Frame[self.Size][5].x = self.Scale * -(8 + (self.Size + 1) * 3)
         self.Frame[self.Size][5].y = self.Scale * +(0 + (self.Size + 1))
         self.Frame[self.Size][6].x = self.Scale * +(8 + (self.Size + 1) * 3)
         self.Frame[self.Size][6].y = self.Scale * +(0 + (self.Size + 1))
         self.Frame[self.Size][7].x = self.Scale * +(8 + (self.Size + 1) * 3)
         self.Frame[self.Size][7].y = self.Scale * -(0 + (self.Size + 1))
         self.Frame[self.Size][8].x = self.Scale * +(8 + (self.Size + 1) * 3)
         self.Frame[self.Size][8].y = self.Scale * +(0 + (self.Size + 1))
         self.Frame[self.Size][9].x = self.Scale * +(0 + (self.Size + 1))
         self.Frame[self.Size][9].y = self.Scale * +(3 + (self.Size + 1) * 3)
         self.Frame[self.Size][10].x = self.Scale * -(0 + (self.Size + 1))
         self.Frame[self.Size][10].y = self.Scale * +(3 + (self.Size + 1) * 3)
         self.Frame[self.Size][11].x = self.Scale * -(8 + (self.Size + 1) * 3)
         self.Frame[self.Size][11].y = self.Scale * +(0 + (self.Size + 1))

      self.Size = self.INACTIVE



   def Draw(self):
      self.Shot.Draw()
      if self.Size != self.INACTIVE:
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
      if self.Shot.Active() == True:
         self.Shot.Move()

      if self.Size != self.INACTIVE:
         if self.Shot.Active() == False:
            self.UFOWav.play()
            self.ShotDirection = random.randrange(4)

            if self.ShotDirection == 0:
               self.Shot.SetArea(self.xMax, self.yMax, self.xOffset, self.yOffset, -8, -8, AstroShot.AstroShot.LARGE_SHOT)
            elif self.ShotDirection == 1:
               self.Shot.SetArea(self.xMax, self.yMax, self.xOffset, self.yOffset, -8, +8, AstroShot.AstroShot.LARGE_SHOT)
            elif self.ShotDirection == 2:
               self.Shot.SetArea(self.xMax, self.yMax, self.xOffset, self.yOffset, +8, -8, AstroShot.AstroShot.LARGE_SHOT)
            elif self.ShotDirection == 3:
               self.Shot.SetArea(self.xMax, self.yMax, self.xOffset, self.yOffset, +8, +8, AstroShot.AstroShot.LARGE_SHOT)

         if random.randrange(10) == 0:
            self.yVelocity = random.randrange((self.Size + 2) * 4) - ((self.Size + 2) * 2)
         if self.xOffset < 0 - self.UFO_WIDTH:
            self.Size = self.INACTIVE
         elif self.xOffset > self.xMax + self.UFO_WIDTH:
            self.Size = self.INACTIVE
         if self.yOffset < 0:
            self.yOffset = 0
         elif self.yOffset > self.yMax:
            self.yOffset = self.yMax
         self.xOffset += self.xVelocity
         self.yOffset += self.yVelocity
      elif random.randrange(1000) == 0:
         self.Size = random.randrange(self.FRAMES)
         self.yOffset = random.randrange(self.yMax)
         if random.randrange(2) == 0:
            self.xOffset = 0 - self.UFO_WIDTH
            self.xVelocity = 3 * (2 - self.Size + 1)
         else:
            self.xOffset = self.xMax + self.UFO_WIDTH
            self.xVelocity = -3 * (2 - self.Size + 1)
         self.yVelocity = random.randrange(2) - 1



   def SetArea(self, Desktop):
      self.xMax = Desktop.width - Desktop.x
      self.yMax = Desktop.height - Desktop.y



   def Collide(self, xPos, yPos, Width, Height):
      self.Collision = False

      if self.Size < self.INACTIVE:
         self.Collision = xPos + Width / 2 > self.xOffset - self.UFO_WIDTH / (self.Size * self.Size + 1) and xPos - Width / 2 < self.xOffset + self.UFO_WIDTH / (self.Size * self.Size + 1) and yPos + Height / 2 > self.yOffset - self.UFO_HEIGHT / (self.Size * self.Size + 1) and yPos - Height / 2 < self.yOffset + self.UFO_HEIGHT / (self.Size * self.Size + 1)
         if self.Collision == True:
            self.Destroy()

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



   def GetShot(self):
      return self.Shot

