# -*- coding: utf-8 -*-
import time
import busio
import board
import adafruit_amg88xx

sensordata = [[27.25, 26.75, 26.75, 27.25, 27.75, 26.75, 27.75, 29.75],
              [27.0,  27.25, 27.25, 26.75, 27.25, 27.5,  29.75, 32.5 ],
              [27.25, 26.5,  26.75, 27.25, 27.0,  27.5,  27.75, 28.75],
              [26.75, 25.5,  26.5,  23.5,  27.0,  24.75, 27.5,  33.5 ],
              [26.75, 26.75, 26.75, 27.0,  27.25, 26.75, 27.25, 32.0 ],
              [26.5,  26.5,  26.5,  27.25, 26.75, 27.0,  28.0,  32.25],
              [26.5,  26.5,  26.5,  27.0,  27.0,  27.25, 28.0,  31.0 ],
              [26.0,  26.5,  26.0,  26.5,  26.5,  26.75, 26.75, 27.75]]

class Sensor():

    def __init__(self):
        # I2Cバスの初期化
        #self.i2c_bus = busio.I2C(board.SCL, board.SDA)

        # センサーの初期化
        #self.amg88sensor = adafruit_amg88xx.AMG88XX(i2c_bus, addr=0x68)
        pass

    def Close(self):
        pass

    def GetData(self):
        #return self.amg88sensor.pixels
        return sensordata

