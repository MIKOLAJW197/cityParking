#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import time

servoPin="P9_14"
PWM.start(servoPin,5,50)


#Configuration czujnika odleglosci
GPIO.setup("P8_12",GPIO.OUT) #Trigger
GPIO.setup("P8_11",GPIO.IN)  #Echo

#SERVO config
servoPin="P9_14"
# PWM.start(servoPin,5,50) TODO Sprawdzic jaki zapis powinien byc
PWM.start(servoPin, 50)

#led config
greenLed = "P8_10"
redLed = "P8_9"
GPIO.setup("P8_10", GPIO.OUT) #green
GPIO.setup("P8_9", GPIO.OUT) #red

#Security
GPIO.output("P8_12", False)
time.sleep(0.5)

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


def openServo():
    desiredAngle = 10
    dutyCycle = 1. / 18. * desiredAngle + 2
    PWM.set_duty_cycle(servoPin, dutyCycle)

def closeServo():
    desiredAngle = 30
    dutyCycle = 1. / 18. * desiredAngle + 2
    PWM.set_duty_cycle(servoPin, dutyCycle)

def ledOn (ledPin):
    GPIO.output(ledPin, GPIO.HIGH)

def ledOff (ledPin):
    GPIO.output(ledPin, GPIO.LOW)

#main Loop
try:
    while True:
        recoveredDistance = distanceMeasurement("P8_12","P8_11")
        print("Distance: " + recoveredDistance + "cm")
        time.sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()