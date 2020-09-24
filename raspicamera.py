# -*- coding: utf-8 -*-
import picamera
import picamera.array

class Camera:

    def __init__(self, width, height, debug):

        # カメラ初期化
        self.camera = picamera.PiCamera()

        # 解像度
        self.camera.resolution = (width, height)

        print("resolution(%i,%i)" % (width,height))

    def start(self):
        self.stream = picamera.array.PiRGBArray(self.camera)

    def capture(self):
        # カメラから映像を取得する（OpenCVへ渡すために、各ピクセルの色の並びをBGRの順番にする）
        self.camera.capture(self.stream, 'bgr', use_video_port=True)
        return self.stream.array.copy()

    def seek(self):
        self.stream.seek(0)
        self.stream.truncate()

    def close(self):
        self.camera.close()





"""
if setting.face_detect == 0:
    # 顔検知OFF
    import pygame
    import pygame.camera
    from pygame.locals import *
else:
    # 顔検知ON
    import picamera
    import picamera.array

def InitCamera( width, height, debug ):
    if setting.face_detect == 0:
        # カメラ初期化
        pygame.camera.init()

        # 解像度
        camera = pygame.camera.Camera("/dev/video0", (width,height))
    else:
        # カメラ初期化
        camera = picamera.PiCamera()

        # 解像度
        camera.resolution = (width, height )

    if debug:
        print("resolution(%i,%i)" % (width,height))

    return camera

#if __name__ == "__main__":
#    InitCamera()
"""
