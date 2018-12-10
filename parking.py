#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from flask import Flask
from flask import request

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

# config of restful-api
app = Flask(__name__)

# note: 1 - wolny/odblokowany , 2 - zajety samochod, 3 - zarezerowwany
parking = [
    {"id": 0,
     "type": "1"},

    {"id": 1,
     "type": "1"}
]


@app.route('/', methods=['GET'])
def api_root():
    if request.method == 'GET':
        return parking, 200


@app.route('/block/<id>', methods=['GET'])
def api_block(id):
    for spot in parking:
        if (id == spot["id"]):
            spot["type"] = 3
    return parking, 200


@app.route('/unblock/<id>', methods=['GET'])
def api_unblock(id):
    for spot in parking:
        if (id == spot["id"]):
            spot["type"] = 1
    return parking, 200


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


def measureDistanceLoop():
    try:
        while True:
            recoveredDistance = distanceMeasurement("P9_12", "P9_15")
            print("Distance: " + recoveredDistance + "cm")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Measurement stopped by user")
        GPIO.cleanup()


# main Loop
if __name__ == '__main__':
    app.run()
