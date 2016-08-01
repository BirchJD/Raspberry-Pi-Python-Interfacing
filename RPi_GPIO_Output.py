#!/usr/bin/python

#/***********************************************/
#/* Raspberry Pi GPIO Output Example in Python. */
#/* 2016-07-31 - Version 1.00 - Jason Birch.    */
#/***********************************************/

import sys
import time
import datetime
import threading
import RPi.GPIO


#/****************************/
#/* USER DEFINABLE CONSTANTS */
#/****************************/
GPIO_OUTPUT_PIN = 14


#  /*******************************************/
# /* Configure Raspberry Pi GPIO interfaces. */
#/*******************************************/
def InitGPIO():
   RPi.GPIO.setmode(RPi.GPIO.BCM)
   RPi.GPIO.setup(GPIO_OUTPUT_PIN, RPi.GPIO.OUT, initial=0)


#  /****************************************/
# /* Procedure to execute every 1 second. */
#/****************************************/
def OutputTimer():
   global OutValue
   global TimerThread

   OutValue = OutValue ^ 1

   RPi.GPIO.output(GPIO_OUTPUT_PIN, OutValue)
   Now = datetime.datetime.now()
   print(Now.strftime("%Y-%m-%d %H:%M:%S") + " - GPIO: " + format(GPIO_OUTPUT_PIN, "00d") + " = " + format(OutValue, "0d"))

   TimerThread = threading.Timer(1, OutputTimer)
   TimerThread.start()


#  /**************************/
# /* Main application loop. */
#/**************************/
Key = 0
OutValue = 0
TimerThread = None

InitGPIO()
OutputTimer()
while Key == 0:
   time.sleep(1)
   Key = sys.stdin.read(1)


#  /*************************************************************************/
# /* Stop the timer so GPIO is not used by mistake after it is cleaned up. */
#/*************************************************************************/
TimerThread.cancel()

#  /*************************************************/
# /* Close Raspberry Pi GPIO use before finishing. */
#/*************************************************/
RPi.GPIO.cleanup()

