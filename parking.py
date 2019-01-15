#!/usr/bin/env python
# -*- coding: utf-8 -*-

import thread
import time
import requests

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

# Configuration czujnika odleglosci
GPIO.setup("P9_12", GPIO.OUT, initial=GPIO.LOW)  # Trigger
GPIO.setup("P9_15", GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Echo

# SERVO config
servoPin = "P9_14"
PWM.start(servoPin, 5, 50)  # NOTE lub bez tej piatki

# led config
greenLed = "P8_10"
redLed = "P8_9"
GPIO.setup("P8_10", GPIO.OUT)  # green
GPIO.setup("P8_9", GPIO.OUT)  # red


# note: 1 - wolny/odblokowany , 2 - zajety samochod, 3 - zarezerowwany
parking = [
    {"id": 1,
     "type": 0}
]


def checkPlace():
    while(1):
        r = requests.get("http://aieozn.pl/sw/isOccupied/1")
        print(r.text)
        time.sleep(2)
        if(r.text == '2' and parking[0]['type'] != 2):
            print('blokada')
            closeServo()
            ledOn(redLed)
            ledOff(greenLed)
            parking[0]['type'] = int(r.text)
        else:
            if(parking[0]['type'] == 2 and r.text != '2'):
                openServo()
                ledOn(greenLed)
                ledOff(redLed)
                print('unblock')
                parking[0]['type'] = int(r.text)



def distanceMeasurement(TRIG, ECHO):
    # Measure the distance between HC-SR04 and nearest wall or solid object.
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)
    pulseStart = time.time()

    while GPIO.input(ECHO) == 0:
        pulseStart = time.time()
    while GPIO.input(ECHO) == 1:
        pulseEnd = time.time()

    pulseDuration = pulseEnd - pulseStart
    distance = pulseDuration * 17150
    distance = round(distance, 2)
    return distance


def openServo():
    dutyCycle = 12
    PWM.set_duty_cycle(servoPin, dutyCycle)


def closeServo():
    dutyCycle = 3
    PWM.set_duty_cycle(servoPin, dutyCycle)


def ledOn(ledPin):
    GPIO.output(ledPin, GPIO.HIGH)


def ledOff(ledPin):
    GPIO.output(ledPin, GPIO.LOW)


def measure_average():
    d1 = distanceMeasurement("P9_12", "P9_15")
    d2 = distanceMeasurement("P9_12", "P9_15")
    d3 = distanceMeasurement("P9_12", "P9_15")
    d4 = distanceMeasurement("P9_12", "P9_15")
    distance = (d1 + d2 + d3 + d4) / 4

    return distance

# main Loop
if __name__ == '__main__':
    # _thread.start_new_thread(serverStart,())
    ledOn(greenLed)
    ledOff(redLed)
    # thread.start_new_thread( checkPlace, ())
    while(1):
        r = requests.get("http://aieozn.pl/sw/isOccupied/1")
        if (r.text != '2'):
            if (parking[0]['type'] == 2):
                openServo()
                ledOn(greenLed)
                ledOff(redLed)
                print('unblock')
                parking[0]['type'] = int(r.text)
            else:
                recoveredDistance = measure_average()
                print('measure distance')
                if (recoveredDistance < 10):
                    ledOff(greenLed)
                    ledOn(redLed)
                    parking[0]['type'] = 1
                    r = requests.get("http://aieozn.pl/sw/take/1")
                    time.sleep(10)
                else:
                    ledOff(redLed)
                    ledOn(greenLed)
                    parking[0]['type'] = 0
                    r = requests.get("http://aieozn.pl/sw/leave/1")
        else:
            if (parking[0]['type'] != 2):
                print('blokada')
                closeServo()
                ledOn(redLed)
                ledOff(greenLed)
                parking[0]['type'] = int(r.text)
            time.sleep(5)
