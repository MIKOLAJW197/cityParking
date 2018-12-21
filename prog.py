#!/usr/bin/env python
# -*- coding: utf-8 -*-

import thread
import time

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS, cross_origin

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
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# note: 1 - wolny/odblokowany , 2 - zajety samochod, 3 - zarezerowwany
parking = [
    {"id": 0,
     "type": "1"},

    {"id": 1,
     "type": "1"}
]


@app.route('/', methods=['GET'])
@cross_origin()
def api_root():
    if request.method == 'GET':
        return jsonify(parking)
#
#
@app.route('/block/<id>', methods=['GET'])
@cross_origin()
def api_block(id):
    for spot in parking:
        if (int(id) == spot['id']):
            spot['type'] = 3
            closeServo()
            ledOff(greenLed)
            ledOn(redLed)

    return jsonify(parking)
#
#
@app.route('/unblock/<id>', methods=['GET'])
@cross_origin()
def api_unblock(id):
    for spot in parking:
        if (int(id) == spot['id']):
            spot['type'] = 1
            openServo()
            ledOff(redLed)
            ledOn(greenLed)
        return jsonify(parking)


# def serverStart():
#     app.run()


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
    time.sleep(1)
    d2 = distanceMeasurement("P9_12", "P9_15")
    time.sleep(1)
    d3 = distanceMeasurement("P9_12", "P9_15")
    time.sleep(1)
    d4 = distanceMeasurement("P9_12", "P9_15")
    distance = (d1 + d2 + d3 + d4) / 4

    return distance

# main Loop
if __name__ == '__main__':
    # _thread.start_new_thread(serverStart,())
    ledOn(greenLed)
    ledOff(redLed)
    while(1):
        if (parking[0]['type'] != 3):
            recoveredDistance = measure_average()
            if (recoveredDistance < 10):
                ledOff(greenLed)
                ledOn(redLed)
                parking[0]['type'] = 2
                time.sleep(10)
            else:
                ledOff(redLed)
                ledOn(greenLed)
                parking[0]['type'] = 1
        else:
            time.sleep(10)
