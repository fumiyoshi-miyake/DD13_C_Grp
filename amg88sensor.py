# -*- coding: utf-8 -*-
import time
import busio
import board
import adafruit_amg88xx

class Sensor():

    def __init__(self):
        # I2Cバスの初期化
        self.i2c_bus = busio.I2C(board.SCL, board.SDA)

        # センサーの初期化
        self.amg88sensor = adafruit_amg88xx.AMG88XX(self.i2c_bus, addr=0x68)

    def Close(self):
        pass

    def start(self):
        pass

    def GetData(self):
        return self.amg88sensor.pixels

