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


import math
import random
import pygame
import Common
import Number
import AstroShot


class AstroShip:
   SCALE = 0.4
   FRAMES = 63
   ERASE_FRAME = FRAMES + 1
   FRAME_POINTS = 5
   THRUST_POINTS = 8
   MAX_X_VELOCITY = 3
   MAX_Y_VELOCITY = 3
   SHIP_WIDTH = 10
   SHIP_HEIGHT = 8
   SHIP_START_ANGLE = 31
   MAX_EXPLODE_FRAME = 45
   LIFE_XGAP = 8
   LIFE_XOFFSET = 48
   LIFE_YOFFSET = 5
   LIVES_SCALE = 0.5
   MAX_LIVES = 3
   SCORE_XOFFSET = 0
   SCORE_YOFFSET = 0
   SCORE_SCALE = 2
   MAX_SHOTS = 10
   HYPERSPACE = -500
   HYPER_FRAMES = 20



   def __init__(self):
      self.Scale = self.SCALE
      self.OneDegree = 6.3 / 360
      self.FrameStep = 0.1      
      self.xMax = 0
      self.yMax = 0
      self.xOffset = self.HYPERSPACE
      self.yOffset = self.HYPERSPACE
      self.xVelocity = 0
      self.yVelocity = 0
      self.Crash = False
      self.ThrustFlag = False
      self.Fade = 0
      self.Lives = self.MAX_LIVES
      self.ExplodeFrame = 0
      self.ShotIndex = 0
      self.HyperCount = False

      self.PlayerScore = Number.Number()

      self.Shots = [AstroShot.AstroShot() for X in range(self.MAX_SHOTS)]
      self.LifeFrame = [Common.XPoint() for X in range(self.FRAME_POINTS)]
      self.LifeDisplayFrame = [Common.XPoint() for X in range(self.FRAME_POINTS)]
      self.Frame = [[Common.XPoint() for X in range(self.FRAME_POINTS)] for Y in range(self.FRAMES)]
      self.DisplayFrame = [Common.XPoint() for X in range(self.FRAME_POINTS * 2)]
      self.OldFrame = [Common.XPoint() for X in range(self.FRAME_POINTS * 2)]
      self.ExplodeDirection = [Common.XPoint() for X in range(self.FRAME_POINTS * 2)]
      self.ThrustTrail = [Common.XPoint() for X in range(self.THRUST_POINTS)]

      self.ShotWav = pygame.mixer.Sound("Sounds/Shot.wav")
      self.ThrustWav = pygame.mixer.Sound("Sounds/Thrust.wav")
      self.ShipBlow = pygame.mixer.Sound("Sounds/ShipBlow.wav")
      self.HyperSpaceWav = pygame.mixer.Sound("Sounds/HyperSpace.wav")

      self.Angle = self.SHIP_START_ANGLE
      self.LifeFrame[0].x = self.Scale * 19 * math.sin(self.FrameStep * self.Angle + self.OneDegree * 0)
      self.LifeFrame[0].y = self.Scale * 19 * math.cos(self.FrameStep * self.Angle + self.OneDegree * 0)
      self.LifeFrame[1].x = self.Scale * 16 * math.sin(self.FrameStep * self.Angle + self.OneDegree * 140)
      self.LifeFrame[1].y = self.Scale * 16 * math.cos(self.FrameStep * self.Angle + self.OneDegree * 140)
      self.LifeFrame[2].x = self.Scale * 8 * math.sin(self.FrameStep * self.Angle + self.OneDegree * 180)
      self.LifeFrame[2].y = self.Scale * 8 * math.cos(self.FrameStep * self.Angle + self.OneDegree * 180)
      self.LifeFrame[3].x = self.Scale * 16 * math.sin(self.FrameStep * self.Angle + self.OneDegree * 220)
      self.LifeFrame[3].y = self.Scale * 16 * math.cos(self.FrameStep * self.Angle + self.OneDegree * 220)
      self.LifeFrame[4].x = self.Scale * 19 * math.sin(self.FrameStep * self.Angle + self.OneDegree * 0)
      self.LifeFrame[4].y = self.Scale * 19 * math.cos(self.FrameStep * self.Angle + self.OneDegree * 0)

      for self.Angle in range(self.FRAMES):
         self.Frame[self.Angle][0].x = self.Scale * 16 * math.sin(self.FrameStep * self.Angle + self.OneDegree * 0)
         self.Frame[self.Angle][0].y = self.Scale * 16 * math.cos(self.FrameStep * self.Angle + self.OneDegree * 0)
         self.Frame[self.Angle][1].x = self.Scale * 13 * math.sin(self.FrameStep * self.Angle + self.OneDegree * 140)
         self.Frame[self.Angle][1].y = self.Scale * 13 * math.cos(self.FrameStep * self.Angle + self.OneDegree * 140)
         self.Frame[self.Angle][2].x = self.Scale * 5 * math.sin(self.FrameStep * self.Angle + self.OneDegree * 180)
         self.Frame[self.Angle][2].y = self.Scale * 5 * math.cos(self.FrameStep * self.Angle + self.OneDegree * 180)
         self.Frame[self.Angle][3].x = self.Scale * 13 * math.sin(self.FrameStep * self.Angle + self.OneDegree * 220)
         self.Frame[self.Angle][3].y = self.Scale * 13 * math.cos(self.FrameStep * self.Angle + self.OneDegree * 220)
         self.Frame[self.Angle][4].x = self.Scale * 16 * math.sin(self.FrameStep * self.Angle + self.OneDegree * 0)
         self.Frame[self.Angle][4].y = self.Scale * 16 * math.cos(self.FrameStep * self.Angle + self.OneDegree * 0)

      self.Angle = self.SHIP_START_ANGLE



   def Draw(self):
      for self.Count in range(self.MAX_SHOTS):
         self.Shots[self.Count].Draw()

      if self.Lives != False or self.ExplodeFrame != self.MAX_EXPLODE_FRAME:
#  /*********************/
# /* Draw intact ship. */
#/*********************/
         if self.Crash == False:
#  /********************************/
# /* Plot ships current position. */
#/********************************/
            for self.Count in range(self.FRAME_POINTS):
               self.DisplayFrame[self.Count].x = self.Frame[self.Angle][self.Count].x + self.xOffset
               self.DisplayFrame[self.Count].y = self.Frame[self.Angle][self.Count].y + self.yOffset

            if self.ExplodeFrame >= self.ERASE_FRAME:
               self.ExplodeFrame = False

#  /************************************/
# /* Erase previous position of ship. */
#/************************************/
               for self.Count in range(0, self.FRAME_POINTS * 2, 2):
                  Common.DrawLine(self.OldFrame[self.Count].x, self.OldFrame[self.Count].y, self.OldFrame[self.Count+1].x, self.OldFrame[self.Count+1].y, 0)

#  /************************************/
# /* Erase previous position of ship. */
#/************************************/
            Common.DrawLines(self.OldFrame, self.FRAME_POINTS, 0)

#  /******************************************/
# /* Draw the ship in the current position. */
#/******************************************/
            Common.DrawLines(self.DisplayFrame, self.FRAME_POINTS, 1)

#  /******************/
# /* Remove thrust. */
#/******************/
            for self.Count in range(self.THRUST_POINTS):
               Common.DrawLine(self.ThrustTrail[self.Count].x, self.ThrustTrail[self.Count].y, self.ThrustTrail[self.Count].x + 1, self.ThrustTrail[self.Count].y + 1, 0)

#  /*****************************************/
# /* Add thrust point if currently active. */
#/*****************************************/
            if self.ThrustFlag == True:
               for self.Count in range(self.THRUST_POINTS):
                  self.ThrustTrail[self.Count].x = self.xOffset + random.randrange(5) - 2 + (9 * math.sin(self.FrameStep * self.Angle + self.OneDegree * 180))
                  self.ThrustTrail[self.Count].y = self.yOffset + random.randrange(5) - 2 + (9 * math.cos(self.FrameStep * self.Angle + self.OneDegree * 180))
                  Common.DrawLine(self.ThrustTrail[self.Count].x, self.ThrustTrail[self.Count].y, self.ThrustTrail[self.Count].x + 1, self.ThrustTrail[self.Count].y + 1, 1)

            self.ThrustFlag = False

#   /******************************************/
#  /* Plot ships current position,           */
# /* next time it will be the old position. */
#/******************************************/
            for self.Count in range(self.FRAME_POINTS):
               self.OldFrame[self.Count].x = self.DisplayFrame[self.Count].x
               self.OldFrame[self.Count].y = self.DisplayFrame[self.Count].y
         else:
            if self.ExplodeFrame == False:
               self.Lives -= 1

#  /************************************/
# /* Erase previous position of ship. */
#/************************************/
               Common.DrawLines(self.OldFrame, self.FRAME_POINTS, 0)

#  /******************/
# /* Remove thrust. */
#/******************/
               for self.Count in range(self.THRUST_POINTS):
                  Common.DrawLine(self.ThrustTrail[self.Count].x, self.ThrustTrail[self.Count].y, self.ThrustTrail[self.Count].x + 1, self.ThrustTrail[self.Count].y + 1, 0)

#  /**************************************************/
# /* Set direction of individual lines of the ship. */
#/**************************************************/
               for self.Count in range(0, self.FRAME_POINTS * 2, 2):
                  self.ExplodeDirection[self.Count].x = 0
                  while self.ExplodeDirection[self.Count].x == 0:
                     self.ExplodeDirection[self.Count].x = random.randrange(10) - 5

                  self.ExplodeDirection[self.Count].y = 0
                  while self.ExplodeDirection[self.Count].y == 0:
                     self.ExplodeDirection[self.Count].y = random.randrange(10) - 5

                  self.ExplodeDirection[self.Count + 1].x = self.ExplodeDirection[self.Count].x
                  self.ExplodeDirection[self.Count + 1].y = self.ExplodeDirection[self.Count].y

#  /********************************************/
# /* Split polygon shape into seperate lines. */
#/********************************************/
               self.DisplayFrame[0].x = self.Frame[self.Angle][self.FRAME_POINTS - 1].x + self.xOffset
               self.DisplayFrame[0].y = self.Frame[self.Angle][self.FRAME_POINTS - 1].y + self.yOffset
               self.OldFrame[0].x = self.Frame[self.Angle][self.FRAME_POINTS - 1].x + self.xOffset
               self.OldFrame[0].y = self.Frame[self.Angle][self.FRAME_POINTS - 1].y + self.yOffset
               self.DisplayFrame[self.FRAME_POINTS * 2 - 1].x = self.Frame[self.Angle][self.FRAME_POINTS - 1].x + self.xOffset
               self.DisplayFrame[self.FRAME_POINTS * 2 - 1].y = self.Frame[self.Angle][self.FRAME_POINTS - 1].y + self.yOffset
               self.OldFrame[self.FRAME_POINTS * 2 - 1].x = self.Frame[self.Angle][self.FRAME_POINTS - 1].x + self.xOffset
               self.OldFrame[self.FRAME_POINTS * 2 - 1].y = self.Frame[self.Angle][self.FRAME_POINTS - 1].y + self.yOffset
               for self.Count in range(self.FRAME_POINTS - 1):
                  self.DisplayFrame[self.Count * 2 + 1].x = self.Frame[self.Angle][self.Count].x + self.xOffset
                  self.DisplayFrame[self.Count * 2 + 1].y = self.Frame[self.Angle][self.Count].y + self.yOffset
                  self.DisplayFrame[self.Count * 2 + 2].x = self.Frame[self.Angle][self.Count].x + self.xOffset
                  self.DisplayFrame[self.Count * 2 + 2].y = self.Frame[self.Angle][self.Count].y + self.yOffset
                  self.OldFrame[self.Count * 2 + 1].x = self.Frame[self.Angle][self.Count].x + self.xOffset
                  self.OldFrame[self.Count * 2 + 1].y = self.Frame[self.Angle][self.Count].y + self.yOffset
                  self.OldFrame[self.Count * 2 + 2].x = self.Frame[self.Angle][self.Count].x + self.xOffset
                  self.OldFrame[self.Count * 2 + 2].y = self.Frame[self.Angle][self.Count].y + self.yOffset
 
#  /************************************/
# /* Erase previous position of ship. */
#/************************************/
            for self.Count in range(0, self.FRAME_POINTS * 2, 2):
               Common.DrawLine(self.OldFrame[self.Count].x, self.OldFrame[self.Count].y, self.OldFrame[self.Count + 1].x, self.OldFrame[self.Count + 1].y, 0)

#  /******************************************/
# /* Draw the ship in the current position. */
#/******************************************/
            if self.ExplodeFrame < self.MAX_EXPLODE_FRAME - 1:
               for self.Count in range(0, self.FRAME_POINTS * 2, 2):
                  self.DisplayFrame[self.Count].x += self.ExplodeDirection[self.Count].x
                  self.DisplayFrame[self.Count].y += self.ExplodeDirection[self.Count].y
                  self.DisplayFrame[self.Count + 1].x += self.ExplodeDirection[self.Count + 1].x
                  self.DisplayFrame[self.Count + 1].y += self.ExplodeDirection[self.Count + 1].y
                  Common.DrawLine(self.DisplayFrame[self.Count].x, self.DisplayFrame[self.Count].y, self.DisplayFrame[self.Count + 1].x, self.DisplayFrame[self.Count + 1].y, 1)

#   /******************************************/
#  /* Plot ships current position,           */
# /* next time it will be the old position. */
#/******************************************/
               for self.Count in range(self.FRAME_POINTS * 2):
                  self.OldFrame[self.Count].x = self.DisplayFrame[self.Count].x
                  self.OldFrame[self.Count].y = self.DisplayFrame[self.Count].y

#  /************************/
# /* Reset for next life. */
#/************************/
            self.ExplodeFrame += 1
            if self.Lives != False and self.ExplodeFrame == self.MAX_EXPLODE_FRAME:
               self.ExplodeFrame = False
               self.Crash = False
               self.ThrustFlag = False
               self.Angle = self.SHIP_START_ANGLE
               self.xOffset = self.xMax / 2
               self.yOffset = self.yMax / 2
               self.xVelocity = 0
               self.yVelocity = 0

#  /****************************/
# /* Display remaining lives. */
#/****************************/
         for self.LifeCount in range(self.MAX_LIVES):
#  /********************************/
# /* Plot ships current position. */
#/********************************/
            for self.Count in range(self.FRAME_POINTS):
               self.LifeDisplayFrame[self.Count].x = self.LIVES_SCALE * self.LifeFrame[self.Count].x + self.LIFE_XOFFSET + (self.LifeCount + 1) * self.LIFE_XGAP
               self.LifeDisplayFrame[self.Count].y = self.LIVES_SCALE * self.LifeFrame[self.Count].y + self.LIFE_YOFFSET

#  /************************************/
# /* Erase previous position of ship. */
#/************************************/
            Common.DrawLines(self.LifeDisplayFrame, self.FRAME_POINTS, 0)

#  /******************************************/
# /* Draw the ship in the current position. */
#/******************************************/
            if self.Lives > self.LifeCount:
               Common.DrawLines(self.LifeDisplayFrame, self.FRAME_POINTS, 1)

#  /******************/
# /* Redraw scores. */
#/******************/
      self.PlayerScore.Draw()



   def IncAngle(self, Direction):
      if self.Crash == False:
         if Direction == False:
            self.Angle += 2
            if self.Angle >= self.FRAMES:
               self.Angle = 0
         else:
            self.Angle -= 2
            if self.Angle < 0:
               self.Angle = self.FRAMES - 1



   def Thrust(self):
      self.ThrustWav.play()
      self.ThrustFlag = True
      self.xVelocity += math.sin(self.FrameStep * self.Angle + self.OneDegree * 0)
      self.yVelocity += math.cos(self.FrameStep * self.Angle + self.OneDegree * 0)
      if self.xVelocity > self.MAX_X_VELOCITY:
         self.xVelocity = self.MAX_X_VELOCITY
      elif self.xVelocity < -self.MAX_X_VELOCITY:
         self.xVelocity = -self.MAX_X_VELOCITY
      if self.yVelocity > self.MAX_Y_VELOCITY:
         self.yVelocity = self.MAX_Y_VELOCITY
      elif self.yVelocity < -self.MAX_Y_VELOCITY:
         self.yVelocity = -self.MAX_Y_VELOCITY



   def Shoot(self):
      if self.Crash == False:
         self.ShotWav.play()
         self.Shots[self.ShotIndex].SetArea(self.xMax, self.yMax, self.xOffset, self.yOffset, self.xVelocity + 10 * math.sin(self.FrameStep * self.Angle + self.OneDegree * 0), self.yVelocity + 10 * math.cos(self.FrameStep * self.Angle + self.OneDegree * 0), AstroShot.AstroShot.SMALL_SHOT)
         self.ShotIndex += 1
         if self.ShotIndex == self.MAX_SHOTS:
            self.ShotIndex = 0



   def Move(self):
      if self.HyperCount != False:
         self.HyperCount -= 1
         if self.HyperCount == False:
            self.xOffset = random.randrange(self.xMax - 2 * self.SHIP_WIDTH)
            self.yOffset = random.randrange(self.yMax - 2 * self.SHIP_HEIGHT)

      for self.Count in range(self.MAX_SHOTS):
         self.Shots[self.Count].Move()

      if self.Crash == False:
         if self.xOffset < 0 - self.SHIP_WIDTH:
            self.xOffset = self.xMax + self.SHIP_WIDTH
         elif self.xOffset > self.xMax + self.SHIP_WIDTH:
            self.xOffset = 0 - self.SHIP_WIDTH
         if self.yOffset < 0 - self.SHIP_HEIGHT:
            self.yOffset = self.yMax + self.SHIP_HEIGHT
         elif self.yOffset > self.yMax + self.SHIP_HEIGHT:
            self.yOffset = 0 - self.SHIP_HEIGHT
         self.xOffset += self.xVelocity
         self.yOffset += self.yVelocity



   def Reset(self):
      if self.Lives == False:
         self.ExplodeFrame = self.ERASE_FRAME
         self.Crash = False
         self.ThrustFlag = False
         self.Fade = 0
         self.Angle = self.SHIP_START_ANGLE
         self.xOffset = self.xMax / 2
         self.yOffset = self.yMax / 2
         self.xVelocity = 0
         self.yVelocity = 0
         self.Lives = self.MAX_LIVES
         self.PlayerScore.SetNumber(0)



   def SetArea(self, Desktop, NewTextColour):
      self.xMax = Desktop.width - Desktop.x
      self.yMax = Desktop.height - Desktop.y
      self.xOffset = self.xMax / 2
      self.yOffset = self.yMax / 2
      self.PlayerScore.SetLocation(self.SCORE_XOFFSET, self.SCORE_YOFFSET, self.SCORE_SCALE, NewTextColour)



   def Hyperspace(self):
      if self.Crash == False and self.HyperCount == False:
         self.HyperSpaceWav.play()
         self.HyperCount = self.HYPER_FRAMES
         self.xOffset = self.HYPERSPACE
         self.yOffset = self.HYPERSPACE
         self.xVelocity = 0
         self.yVelocity = 0



   def Collide(self, xPos, yPos, Width, Height):
      self.Collision = False

      if self.Crash == False:
         self.Collision = xPos + Width / 2 > self.xOffset - self.SHIP_WIDTH and xPos - Width / 2 < self.xOffset + self.SHIP_WIDTH and yPos + Height / 2 > self.yOffset - self.SHIP_HEIGHT and yPos - Height / 2 < self.yOffset + self.SHIP_HEIGHT
         if self.Collision == True:
            self.Crash = True

      return self.Collision



   def SetCrash(self, NewCrash):
      if self.Crash == False and NewCrash == True:
         self.ShipBlow.play()
      self.Crash = NewCrash



   def GetCrash(self):
      return self.Crash



   def GetXOffset(self):
      return self.xOffset



   def GetYOffset(self):
      return self.yOffset



   def GetWidth(self):
      return self.SHIP_WIDTH



   def GetHeight(self):
      return self.SHIP_HEIGHT



   def GetScore(self):
      return self.PlayerScore.GetNumber()



   def SetScore(self, NewScore):
      self.PlayerScore.SetNumber(NewScore)



   def GetLives(self):
      return self.Lives



   def GetShot(self, ShotCount):
      return self.Shots[ShotCount]



   def GetShotCount(self):
      return self.MAX_SHOTS

