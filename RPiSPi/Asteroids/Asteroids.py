#!/usr/bin/python

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


import time
import random
import pygame
import Common
import Text
import Number
import AstroShot
import AstroShip
import AstroUFO
import AstroRock


#  /*********************/
# /* Define constants. */
#/*********************/
EVENT_TIMER = pygame.USEREVENT + 1

START_ROCKS = 2
MAX_ROCKS = 100
HISCORE_XOFFSET = 90
HISCORE_YOFFSET = 0
GAMEOVER_XOFFSET = 34
GAMEOVER_YOFFSET = 5
INSERTCOIN_XOFFSET = 45
INSERTCOIN_YOFFSET = 5
HISCORE_SCALE = 2

GPIO_KEY_ESC    = 0b0001000000000000
GPIO_KEY_START  = 0b0010000000000000
GPIO_KEY_SHOOT  = 0b1000000000000000
GPIO_KEY_LEFT   = 0b0000000000000100
GPIO_KEY_RIGHT  = 0b0000000000001000
GPIO_KEY_THRUST = 0b0100000000000000

GPIO_KEY_HYPER  = 0b0010000000000000


#  /********************/
# /* Set random seed. */
#/********************/
random.seed(time.gmtime())

#  /*******************************/
# /* Initialise game components. */
#/*******************************/
pygame.init()
pygame.mixer.init()

Common.InitSPI()

#  /*****************/
# /* Game objects. */
#/*****************/
Ship = AstroShip.AstroShip()
UFO = AstroUFO.AstroUFO()
Rock = [AstroRock.AstroRock() for X in range(MAX_ROCKS)]
HiScore = Number.Number()
GameOver = Text.Text()
InsertCoin = Text.Text()

#  /***************/
# /* Game flags. */
#/***************/
Exit = False
SetFlag = False
ThrustFlag = False
RotateLeftFlag = False
RotateRightFlag = False



def DrawGraphics():
#  /*******************************/
# /* Draw ship and rock objects. */
#/*******************************/
   InsertCoin.Draw()
   GameOver.Draw()
   HiScore.Draw()
   Ship.Draw()
   UFO.Draw()
   for Count in range(MAX_ROCKS):
      Rock[Count].Draw()

   Common.DrawUpdate()



def Timer():
   global FirstRock
   global NextRock

   if ThrustFlag:
      Ship.Thrust()
   elif RotateLeftFlag:
      Ship.IncAngle(False)
      Ship.IncAngle(False)
   elif RotateRightFlag:
      Ship.IncAngle(True)
      Ship.IncAngle(True)

   Ship.Move()
   UFO.Move()
   RockFound = False
   for Count in range(MAX_ROCKS):
      if Rock[Count].GetSize() != AstroRock.AstroRock.INACTIVE:
         RockFound = True

#  /*****************************/
# /* Check for ship collision. */
#/*****************************/
      if Ship.GetCrash() == False and UFO.Collide(Ship.GetXOffset(), Ship.GetYOffset(), Ship.GetWidth(), Ship.GetHeight()) == True:
         Ship.SetCrash(True)
      if UFO.GetShot().Active() == True and Ship.Collide(UFO.GetShot().GetXOffset(), UFO.GetShot().GetYOffset(), 2, 2) == True:
         Ship.SetCrash(True)
      if Ship.GetCrash() == False and Rock[Count].Collide(Ship.GetXOffset(), Ship.GetYOffset(), Ship.GetWidth(), Ship.GetHeight()) == True:
         Ship.SetCrash(True)
         NextRock += 1
         Rock[NextRock].SetArea(Common.Desktop, Ship.GetXOffset(), Ship.GetYOffset(), Rock[Count].GetSize())

#  /*************************/
# /* Check for shot rocks. */
#/*************************/
      for ShotCount in range(Ship.GetShotCount()):
         if Ship.GetShot(ShotCount).Active() != False:
            if UFO.Collide(Ship.GetShot(ShotCount).GetXOffset(), Ship.GetShot(ShotCount).GetYOffset(), 2, 2) == True:
               Ship.SetScore(Ship.GetScore() + 10)
               Ship.GetShot(ShotCount).Destroy()
            if Rock[Count].Collide(Ship.GetShot(ShotCount).GetXOffset(), Ship.GetShot(ShotCount).GetYOffset(), 2, 2) == True:
               Ship.SetScore(Ship.GetScore() + 1 * Rock[Count].GetSize())
               Ship.GetShot(ShotCount).Destroy()
               if NextRock + 1 < MAX_ROCKS:
                  NextRock += 1
                  Rock[NextRock].SetArea(Common.Desktop, Rock[Count].GetXOffset(), Rock[Count].GetYOffset(), Rock[Count].GetSize())

      Rock[Count].Move()

   if RockFound == False:
      FirstRock += 1
      NextRock = FirstRock
      for Count in range(FirstRock):
         Rock[Count].SetArea(Common.Desktop, AstroRock.AstroRock.NEW_POSITION, AstroRock.AstroRock.NEW_POSITION, 0)

   GameOver.SetVisible(Ship.GetLives() == False)
   InsertCoin.SetVisible(GameOver.GetVisible() == False and Ship.GetLives() == False)

   DrawGraphics()



#  /*****************************/
# /* Configure game variables. */
#/*****************************/
GameOver = Text.Text()
GameOver.SetLocation((Common.Desktop.width - Common.Desktop.x) / 2 - GAMEOVER_XOFFSET, (Common.Desktop.height - Common.Desktop.y) / 2 - GAMEOVER_YOFFSET, 2, 200, False, "GAME OVER", 1)

InsertCoin = Text.Text()
InsertCoin.SetLocation((Common.Desktop.width - Common.Desktop.x) / 2 - INSERTCOIN_XOFFSET, (Common.Desktop.height - Common.Desktop.y) / 2 - INSERTCOIN_YOFFSET, 2, 15, True, "INSERT COIN", 1)

HiScore = Number.Number()
HiScore.SetLocation(HISCORE_XOFFSET, HISCORE_YOFFSET, HISCORE_SCALE, 1)

Ship = AstroShip.AstroShip()
Ship.SetArea(Common.Desktop, 1)

UFO = AstroUFO.AstroUFO()
UFO.SetArea(Common.Desktop)

FirstRock = START_ROCKS
NextRock = FirstRock
for Count in range(FirstRock):
   Rock[Count].SetArea(Common.Desktop, AstroRock.AstroRock.NEW_POSITION, AstroRock.AstroRock.NEW_POSITION, 0)

#  /**************************************************************/
# /* Process application messages until the ESC key is pressed. */
#/**************************************************************/
pygame.time.set_timer(EVENT_TIMER, 100)
ShotKeyFlag = False
LastShotKeyFlag = False
ExitFlag = False
while ExitFlag == False:
#  /*************************************/
# /* Yeald for other processes to run. */
#/*************************************/
   pygame.time.wait(25)

#  /************************************/
# /* Process application event queue. */
#/************************************/
   for ThisEvent in pygame.event.get():
#  /******************************************************************/
# /* If ptyhon has posted a QUIT message, flag to exit applicaiton. */
#/******************************************************************/
      if ThisEvent.type == pygame.QUIT:
         ExitFlag = True
         break

#  /*********************************************************/
# /* On timer period perform one frame of the application. */
#/*********************************************************/
      elif ThisEvent.type == EVENT_TIMER:

         Timer()

#  /*************************/
# /* Update display frame. */
#/*************************/
         DrawGraphics()

#  /****************************************************************/
# /* Check for ESC key press, and exit application when detected. */
#/****************************************************************/
         KeysPressed = Common.GetGpioKeys()

#  /****************************/
# /* Handle key press events. */
#/****************************/
         if KeysPressed & GPIO_KEY_ESC:
            ExitFlag = True
            break

#  /****************************/
# /* 'Ctrl' key press, shoot. */
#/****************************/
         if KeysPressed & GPIO_KEY_SHOOT:
            ShotKeyFlag = True
         else:
            ShotKeyFlag = False
         if ShotKeyFlag != LastShotKeyFlag:
            Ship.Shoot()
         LastShotKeyFlag = ShotKeyFlag

#  /***************************/
# /* 'up' key press, thrust. */
#/***************************/
         if KeysPressed & GPIO_KEY_THRUST:
            ThrustFlag = True
         else:
            ThrustFlag = False

#  /**********************************/
# /* 'left' key press, rotate left. */
#/**********************************/
         if KeysPressed & GPIO_KEY_LEFT:
            RotateLeftFlag = True
         else:
            RotateLeftFlag = False

#  /************************************/
# /* 'right' key press, rotate right. */
#/************************************/
         if KeysPressed & GPIO_KEY_RIGHT:
            RotateRightFlag = True
         else:
            RotateRightFlag = False

#  /*********************************/
# /* 'down' key press, hyperspace. */
#/*********************************/
         if KeysPressed & GPIO_KEY_HYPER:
            Ship.Hyperspace()

#  /*****************************/
# /* 'F1' key press, new game. */
#/*****************************/
         if KeysPressed & GPIO_KEY_START:
            if Ship.GetLives() == False:
               if Ship.GetScore() > HiScore.GetNumber():
                  HiScore.SetNumber(Ship.GetScore())
               Ship.Reset()
               UFO.Destroy()
               UFO.GetShot().Destroy()
               FirstRock = START_ROCKS
               NextRock = FirstRock
               for Count in range(MAX_ROCKS):
                  Rock[Count].Destroy()
               for Count in range(FirstRock):
                  Rock[Count].SetArea(Common.Desktop, AstroRock.AstroRock.NEW_POSITION, AstroRock.AstroRock.NEW_POSITION, 0)

#  /*****************/
# /* Stop threads. */
#/*****************/
ExitFlag = True

#  /*********************************/
# /* Application clean up and end. */
#/*********************************/
Common.CloseSPI()

pygame.time.set_timer(EVENT_TIMER, 0)
pygame.mouse.set_visible(True)

