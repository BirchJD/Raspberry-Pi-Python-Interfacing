#!/usr/bin/python2

# RPi_MCP3002_TempSense - Python Example Using RPiSPi Driver and MCP3002
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
#/* RPiSPi_MCP3002                                                           */
#/* ------------------------------------------------------------------------ */
#/* V1.00 - 2016-11-02 - Jason Birch                                         */
#/* ------------------------------------------------------------------------ */
#/* Python Example Using RPiSPi Driver and MCP3002 A-D Converter to read     */
#/* temprature sensors.                                                      */
#/* cat Device.cfg >/dev/RPiSPi                                              */
#/* cat /proc/RPiSPi                                                         */
#/****************************************************************************/


import sys
import time
import math
import datetime
import struct
import pygame


#  /*********************/
# /* Define constants. */
#/*********************/
# PLOT_HOURS = 0.05
PLOT_HOURS = 1.0
# PLOT_HOURS = 24.0

AD_REF_VOLTAGE = 3.3
AD_RESOLUTION = 1024.0
CAL_VALUES = 101
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
GRAPH_TOP = 20.0
GRAPH_LEFT = 40.0
GRAPH_HEIGHT = 400.0
GRAPH_WIDTH = 590.0
SUB_GRAPH_TOP = 20.0
SUB_GRAPH_LEFT = 530.0
SUB_GRAPH_HEIGHT = 100.0
SUB_GRAPH_SCALE_X = 1.0
SUB_GRAPH_SCALE_Y = 0.1

WHITE_COLOUR = (0xFF, 0xFF, 0xFF)
GREY_COLOUR = (0x7F, 0x7F, 0x7F)
DIM_GREY_COLOUR = (0x50, 0x50, 0x50)
BLACK_COLOUR = (0x00, 0x00, 0x00)
MCP9701A_CAL_COLOUR = (0x00, 0x7F, 0x00)
MCP9701A_TEMPRATURE_COLOUR = (0x50, 0xFF, 0x50)
THERMISTOR_CAL_ADJ_COLOUR = (0x7F, 0x00, 0x00)
THERMISTOR_CAL_OFFSET_COLOUR = (0x7F, 0x00, 0x00)
THERMISTOR_CAL_COLOUR = (0x00, 0x00, 0x7F)
THERMISTOR_TEMPRATURE_COLOUR = (0x00, 0x00, 0x7F)
THERMISTOR_TEMPRATURE_COLOUR_ADJ = (0x50, 0x50, 0xFF)

EVENT_TIMER = pygame.USEREVENT + 1



def ReadAD(DevFile):
   File = open(DevFile, 'rb', 0)
   Data = File.read(4)
   File.close()
   return struct.unpack("<%dI" % (len(Data) // 4), Data)[0]


def Timer():
   global X
   global Y0
   global Y1
   global Y1Adjusted

#  /***************************************************/
# /* Read A-D channel 0, MCP9701A temprature sensor. */
#/***************************************************/
   Value0 = ReadAD("/dev/RPiSPi_0001_000_0_2_MCP3002_READ0")
# Calculate the voltage value, 3V3 maximum scale, 1024 reading maximum scale.
   ValueVolt0 = AD_REF_VOLTAGE * Value0 / AD_RESOLUTION
# Calculate the temprature, 0C = 0.4V, each 1C = 19.5mV, from data sheet.
   Value0C = (ValueVolt0 - 0.4) / 0.0195

#  /****************************************/
# /* Read A-D channel 1, 100K Thermister. */
#/****************************************/
   Value1 = ReadAD("/dev/RPiSPi_0001_000_0_3_MCP3002_READ1")
# Calculate the voltage value, 3V3 maximum scale, 1024 reading maximum scale.
   ValueVolt1 = AD_REF_VOLTAGE * Value1 / AD_RESOLUTION
# From calibrating with ice water, 0C = 250 A-D reading.
   Value1Zero = 260.0
# From calibrating with hot water and MCP9701A reading, 50C = 745 A-D reading.
   Value1Fifty = 670.0
# From calibrating with boiling water, 100C = 1200 A-D reading.
   Value1Hundred = 1070.0
# Calculate 50C reading as a value in the range 0 - 1 (equivelent 0C - 100C).
   Value1MidPoint = (Value1Fifty - Value1Zero) / (Value1Hundred - Value1Zero) * 100
# Calculate unadjusted read value in the range 0 - 1 (equivelent 0C - 100C).
   Value1C = (Value1 - Value1Zero) / (Value1Hundred - Value1Zero) * 100
# Look up adjusted value on a sin curve of points calibration.
   CurveY =  200.0 + (math.cos(1.0 + Value1C / 65.0) + 0.0175 * Value1C) * Value1Hundred
   Value1CAdjusted = (CurveY - Value1Zero) / (Value1Hundred - Value1Zero) * 250 - 167

#   /*****************************************/
#  /* If a new calibration value is found,  */
# /* add it and save the calibration data. */ 
#/*****************************************/
   if int(Value0C) >= 0 and int(Value0C) <= 100 and (MCP9701A_Values[int(Value0C)][1] == 0 or Thermister_Values[int(Value0C)][1] == 0):
      MCP9701A_Values[int(Value0C)] = (int(Value0C), Value0)
      Thermister_Values[int(Value0C)] = (int(Value0C), Value1)

      try:
         File = open("CalValues.txt", 'w', 0)
         for Count in range(CAL_VALUES):
            File.write(str(Count) + ",")
            File.write(str(MCP9701A_Values[Count][1]) + ",")
            File.write(str(Thermister_Values[Count][1]) + "\n")
         File.close()
      except:
         print("")

#  /******************/
# /* Clear display. */
#/******************/
   ThisSurface.fill(BLACK_COLOUR)

#  /*********************************************/
# /* Draw MCP9701A collected calibration data. */
#/*********************************************/
   LastY = 0
   LastCurveY = 0
   LastYAdjusted = 0
   for Count in range(CAL_VALUES - 1):
# MCP9701A calibration data.
      if MCP9701A_Values[Count][1] > 0 and MCP9701A_Values[Count + 1][1] > 0:
         pygame.draw.line(ThisSurface, MCP9701A_CAL_COLOUR, (SUB_GRAPH_LEFT + SUB_GRAPH_SCALE_X * MCP9701A_Values[Count][0], SUB_GRAPH_TOP + SUB_GRAPH_HEIGHT - MCP9701A_Values[Count][1] * SUB_GRAPH_SCALE_Y), (SUB_GRAPH_LEFT + SUB_GRAPH_SCALE_X * MCP9701A_Values[Count + 1][0], SUB_GRAPH_TOP + SUB_GRAPH_HEIGHT - MCP9701A_Values[Count + 1][1] * SUB_GRAPH_SCALE_Y), 1)
# Thermistor calibration data.
      if Thermister_Values[Count][1] > 0 and Thermister_Values[Count + 1][1] > 0:
         pygame.draw.line(ThisSurface, THERMISTOR_CAL_COLOUR, (SUB_GRAPH_LEFT + SUB_GRAPH_SCALE_X * Thermister_Values[Count][0], SUB_GRAPH_TOP + SUB_GRAPH_HEIGHT - Thermister_Values[Count][1] * SUB_GRAPH_SCALE_Y), (SUB_GRAPH_LEFT + SUB_GRAPH_SCALE_X * Thermister_Values[Count + 1][0], SUB_GRAPH_TOP + SUB_GRAPH_HEIGHT - Thermister_Values[Count + 1][1] * SUB_GRAPH_SCALE_Y), 1)

# Calibration adjustment to convert 100K Thermistor to approx MCP9701A values.
# Manipulate sin wav to cancel out inaccuracies.

# Thermistor calibration approximated curve.
      CurveY =  200.0 + (math.cos(1.0 + Count / 65.0) + 0.0175 * Count) * Value1Hundred
      if Count > 0:
         pygame.draw.line(ThisSurface, THERMISTOR_CAL_ADJ_COLOUR, (SUB_GRAPH_LEFT + SUB_GRAPH_SCALE_X * Count, SUB_GRAPH_TOP + SUB_GRAPH_HEIGHT - LastCurveY * SUB_GRAPH_SCALE_Y), (SUB_GRAPH_LEFT + SUB_GRAPH_SCALE_X * (Count + 1), SUB_GRAPH_TOP + SUB_GRAPH_HEIGHT - CurveY * SUB_GRAPH_SCALE_Y), 1)

# Thermistor calibration adjutment offsets.
      if Thermister_Values[Count][1] == 0:
         Y = Thermister_Values[Count][1]
      else:
         Y = CurveY - Thermister_Values[Count][1]
      if Count > 0:
         pygame.draw.line(ThisSurface, THERMISTOR_CAL_OFFSET_COLOUR, (SUB_GRAPH_LEFT + SUB_GRAPH_SCALE_X * Count, SUB_GRAPH_TOP + SUB_GRAPH_HEIGHT - LastY * SUB_GRAPH_SCALE_Y), (SUB_GRAPH_LEFT + SUB_GRAPH_SCALE_X * (Count + 1), SUB_GRAPH_TOP + SUB_GRAPH_HEIGHT - Y * SUB_GRAPH_SCALE_Y), 1)

# Adjusted thermistor calibrated data.
      YAdjusted =  (Thermister_Values[Count][1] + CurveY) / 2 - 100
      if Count > 0:
         pygame.draw.line(ThisSurface, WHITE_COLOUR, (SUB_GRAPH_LEFT + SUB_GRAPH_SCALE_X * Count, SUB_GRAPH_TOP + SUB_GRAPH_HEIGHT - LastYAdjusted * SUB_GRAPH_SCALE_Y), (SUB_GRAPH_LEFT + SUB_GRAPH_SCALE_X * (Count + 1), SUB_GRAPH_TOP + SUB_GRAPH_HEIGHT - YAdjusted * SUB_GRAPH_SCALE_Y), 1)

      LastY = Y
      LastCurveY = CurveY
      LastYAdjusted = YAdjusted

#  /***************************************************/
# /* Draw A-D channel 0, MCP9701A temprature sensor. */
#/***************************************************/
   Y0[X] = ((GRAPH_LEFT + X, GRAPH_TOP + GRAPH_HEIGHT - Value0C / 100.0 * GRAPH_HEIGHT))
   pygame.draw.lines(ThisSurface, MCP9701A_TEMPRATURE_COLOUR, False, Y0, 1)

#  /****************************************/
# /* Draw A-D channel 1, 100K Thermister. */
#/****************************************/
   Y1[X] = ((GRAPH_LEFT + X, GRAPH_TOP + GRAPH_HEIGHT - Value1C / 100.0 * GRAPH_HEIGHT))
   Y1Adjusted[X] = ((GRAPH_LEFT + X, GRAPH_TOP + GRAPH_HEIGHT - Value1CAdjusted / 100.0 * GRAPH_HEIGHT))
   pygame.draw.lines(ThisSurface, THERMISTOR_TEMPRATURE_COLOUR, False, Y1, 1)
   pygame.draw.lines(ThisSurface, THERMISTOR_TEMPRATURE_COLOUR_ADJ, False, Y1Adjusted, 1)

#  /************************/
# /* Display graph title. */
#/************************/
   DisplayText = "MCP9701A TEMPRATURE SENSOR"
   FontText = SmallFont.render(DisplayText, True, MCP9701A_TEMPRATURE_COLOUR)
   ThisSurface.blit(FontText, (110, 0))

   DisplayText = "vs"
   FontText = SmallFont.render(DisplayText, True, GREY_COLOUR)
   ThisSurface.blit(FontText, (380, 0))

   DisplayText = "100K THERMISTOR"
   FontText = SmallFont.render(DisplayText, True, THERMISTOR_TEMPRATURE_COLOUR)
   ThisSurface.blit(FontText, (410, 0))

#  /*****************************/
# /* Display current readings. */
#/*****************************/
   Now = datetime.datetime.now()
   DisplayText = Now.strftime("%Y-%m-%d %H:%M:%S")
#   print(DisplayText)
   FontText = SmallFont.render(DisplayText, True, WHITE_COLOUR)
   ThisSurface.blit(FontText, (10, 450))

   DisplayText = "AD0=" + "{0:4}".format(Value0) + " " + "{0:7.4}".format(ValueVolt0) + "V, " + "{0:6.3}".format(Value0C) + "C"
#   print(DisplayText)
   FontText = SmallFont.render(DisplayText, True, MCP9701A_TEMPRATURE_COLOUR)
   ThisSurface.blit(FontText, (170, 450))

   DisplayText = "AD1=" + "{0:4}".format(Value1) + " " + "{0:7.4}".format(ValueVolt1) + "V, " + "{0:6.3}".format(Value1C) + "C [" + "{0:6.3}".format(Value1CAdjusted) + "C]"
#   print(DisplayText)
   FontText = SmallFont.render(DisplayText, True, THERMISTOR_TEMPRATURE_COLOUR_ADJ)
   ThisSurface.blit(FontText, (380, 450))

#  /********************/
# /* Draw graph axis. */
#/********************/
   pygame.draw.line(ThisSurface, GREY_COLOUR, (GRAPH_LEFT, GRAPH_TOP), (GRAPH_LEFT, GRAPH_TOP + GRAPH_HEIGHT), 1)
   pygame.draw.line(ThisSurface, GREY_COLOUR, (GRAPH_LEFT, GRAPH_TOP + GRAPH_HEIGHT), (GRAPH_LEFT + GRAPH_WIDTH, GRAPH_TOP + GRAPH_HEIGHT), 1)
   pygame.draw.line(ThisSurface, WHITE_COLOUR, (GRAPH_LEFT + 1 + X, GRAPH_TOP), (GRAPH_LEFT + 1 + X, GRAPH_TOP + GRAPH_HEIGHT), 1)
   pygame.draw.line(ThisSurface, DIM_GREY_COLOUR, (SUB_GRAPH_LEFT + SUB_GRAPH_SCALE_X * Value1C, SUB_GRAPH_TOP), (SUB_GRAPH_LEFT + SUB_GRAPH_SCALE_X * Value1C, SUB_GRAPH_TOP + SUB_GRAPH_HEIGHT), 1)

#  /*****************/
# /* Draw Y scale. */
#/*****************/
   for Count in range(0, 110, 10):
      Ypos = GRAPH_TOP + GRAPH_HEIGHT - Count / 100.0 * GRAPH_HEIGHT
      pygame.draw.line(ThisSurface, GREY_COLOUR, (GRAPH_LEFT - 5, Ypos), (GRAPH_LEFT, Ypos), 1)
      FontText = SmallFont.render("{0:3}".format(Count), True, GREY_COLOUR)
      ThisSurface.blit(FontText, (5, Ypos - 10))

#  /*****************/
# /* Draw X scale. */
#/*****************/
   XStep = PLOT_HOURS / 6.0
   Count = 0.0
   while Count <= PLOT_HOURS:
      Xpos = GRAPH_LEFT + Count * GRAPH_WIDTH / PLOT_HOURS
      pygame.draw.line(ThisSurface, GREY_COLOUR, (Xpos, GRAPH_TOP + GRAPH_HEIGHT), (Xpos, GRAPH_TOP + GRAPH_HEIGHT + 5), 1)
      FontText = SmallFont.render("{0:3.3}".format(Count), True, GREY_COLOUR)
      ThisSurface.blit(FontText, (Xpos - 20, GRAPH_TOP + GRAPH_HEIGHT + 10))
      Count += XStep

#  /*******************/
# /* Update display. */
#/*******************/
   pygame.display.flip()
   X += 1
   if X > GRAPH_WIDTH:
      X = 0



#  /***************/
# /* Initialize. */
#/***************/
pygame.init()
ThisSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
SmallFont = pygame.font.Font(None, 22)
ThisSurface.fill(BLACK_COLOUR)
pygame.display.flip()

X = 0
Y0 = [(GRAPH_LEFT + Value, GRAPH_TOP + GRAPH_HEIGHT) for Value in range(int(GRAPH_WIDTH) + 1)]
Y1 = [(GRAPH_LEFT + Value, GRAPH_TOP + GRAPH_HEIGHT) for Value in range(int(GRAPH_WIDTH) + 1)]
Y1Adjusted = [(GRAPH_LEFT + Value, GRAPH_TOP + GRAPH_HEIGHT) for Value in range(int(GRAPH_WIDTH) + 1)]
Thermister_Values = [(GRAPH_LEFT + Value, 0) for Value in range(CAL_VALUES)]
MCP9701A_Values = [(GRAPH_LEFT + Value, 0) for Value in range(CAL_VALUES)]

#  /***************************************/
# /* Load last saved calibration values. */
#/***************************************/
try:
   File = open("CalValues.txt", 'r', 0)
   for Count in range(CAL_VALUES):
      TextLine = File.readline()
      if not TextLine:
         break
      Values = TextLine.split(",")
      MCP9701A_Values[int(Values[0])] = (int(Values[0]), int(Values[1]))
      Thermister_Values[int(Values[0])] = (int(Values[0]), int(Values[2]))
   File.close()
except:
   print("")

#  /**************************************************************/
# /* Process application messages until the ESC key is pressed. */
#/**************************************************************/
ExitFlag = False
Timer()
pygame.time.set_timer(EVENT_TIMER, int(PLOT_HOURS * 6125.0))
while ExitFlag == False:
#  /*************************************/
# /* Yeald for other processes to run. */
#/*************************************/
   pygame.time.wait(100)

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

#  /****************************************************************/
# /* Check for ESC key press, and exit application when detected. */
#/****************************************************************/
      KeysPressed = pygame.key.get_pressed()
      if KeysPressed[pygame.K_ESCAPE]:
         ExitFlag = True


#  /*********************************/
# /* Application clean up and end. */
#/*********************************/
pygame.time.set_timer(EVENT_TIMER, 0)

