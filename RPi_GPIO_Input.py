#!/usr/bin/python

#/**********************************************/
#/* Raspberry Pi GPIO Input Example in Python. */
#/* 2016-07-31 - Version 1.00 - Jason Birch.   */
#/**********************************************/

import sys
import time
import datetime
import RPi.GPIO


#/****************************/
#/* USER DEFINABLE CONSTANTS */
#/****************************/
GPIO_INPUT_PIN = 14


#  /*******************************************/
# /* Configure Raspberry Pi GPIO interfaces. */
#/*******************************************/
def InitGPIO():
   RPi.GPIO.setmode(RPi.GPIO.BCM)
   RPi.GPIO.setup(GPIO_INPUT_PIN, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
   RPi.GPIO.add_event_detect(GPIO_INPUT_PIN, RPi.GPIO.RISING, callback=InputCallback, bouncetime=200)
#   RPi.GPIO.add_event_detect(GPIO_INPUT_PIN, RPi.GPIO.FALLING, callback=InputCallback, bouncetime=200)


#  /**************************************/
# /* Raspberry Pi GPIO interupt routine. */
#/**************************************/
def InputCallback(GpioPin):
   Now = datetime.datetime.now()
   print(Now.strftime("%Y-%m-%d %H:%M:%S") + " - GPIO: " + format(GpioPin, "00d"))



#  /**************************/
# /* Main application loop. */
#/**************************/
InitGPIO()
Key = 0
while Key == 0:
   time.sleep(1)
   Key = sys.stdin.read(1)


#  /*************************************************/
# /* Close Raspberry Pi GPIO use before finishing. */
#/*************************************************/
RPi.GPIO.cleanup()

