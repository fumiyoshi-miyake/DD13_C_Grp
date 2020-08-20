# -*- coding: utf-8 -*-
import time
import busio
import board
import adafruit_amg88xx

def InitSensor( debug ):
    # I2Cバスの初期化
    i2c_bus = busio.I2C(board.SCL, board.SDA)

    # センサーの初期化
    sensor = adafruit_amg88xx.AMG88XX(i2c_bus, addr=0x68)

    return sensor
