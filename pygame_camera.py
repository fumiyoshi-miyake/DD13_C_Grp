# -*- coding: utf-8 -*-
import pygame
import pygame.camera
from pygame.locals import *

class Camera:

    def __init__(self, width, height, debug):

        # カメラ初期化
        pygame.camera.init()

        # 解像度
        self.camera = pygame.camera.Camera("/dev/video0", (width,height))

        print("Pygame resolution(%i,%i)" % (width,height))

    def start(self):
        self.camera.start()

    # キャプチャー
    def capture(self):
        return self.camera.get_image()

    def seek(self):
        pass

    def close(self):
        self.camera.stop()
