#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Adafruit_BBIO.GPIO as GPIO
import time

def distanceMeasurement(TRIG,ECHO):

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulseStart = time.time()
    while GPIO.input(ECHO) == 1:
        pulseEnd = time.time()

    pulseDuration = pulseEnd - pulseStart
    distance = pulseDuration * 17150
    distance = round(distance, 2)
    return distance

#Configuration
GPIO.setup("P8_12",GPIO.OUT) #Trigger
GPIO.setup("P8_11",GPIO.IN)  #Echo

#Security
GPIO.output("P8_12", False)
time.sleep(0.5)

#main Loop
try:
    while True:
        recoveredDistance = distanceMeasurement("P8_12","P8_11")
        print("Distance: " + recoveredDistance + "cm")
        time.sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()