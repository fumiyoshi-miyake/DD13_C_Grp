# -*- coding: utf-8 -*-
import picamera
import picamera.array

def InitCamera( width, height, debug ):
    # カメラ初期化
    camera = picamera.PiCamera()

    # 解像度
    camera.resolution = (width, height )
    if debug:
        print("resolution(%i,%i)" % (width,height))

    return camera

#if __name__ == "__main__":
#    InitCamera()
