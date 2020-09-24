import sys
import time
import numpy as np
import cv2
import pygame
import pygame.camera
from pygame.locals import *

import setting
import module
import GetBodyTempData

#from pygame_util import *
from pygame_util import open_disp
from pygame_util import make_colorbar
from pygame_util import convert_opencv_img_to_pygame
from pygame_util import out_disp
from pygame_util import close_disp
from pygame_util import startMsg_disp

from calc import measure
from calc import AVERAGE_COUNT
    

# 初期化
BodyTempArray = [0] * AVERAGE_COUNT
BodyTempIndex = 0
SeqCount = 0

# 実機
if setting.mode == 0:
    # 公開ライブラリ又はファイルインポート
    if setting.face_detect == 0:
        # 顔検知OFF
        import pygame
        import pygame.camera
        from pygame.locals import *
    else:
        # 顔検知ON
        import picamera
        import picamera.array

    if setting.sensor == 0:
        # AMG88センサ
        import adafruit_amg88xx 

    # ローカルファイルインポート
    if setting.face_detect == 0:
        # 顔検知OFF
        import pygame_camera
    else:
        # 顔検知ON
        import raspicamera

    if setting.sensor == 0:
        # AMG88センサ
        import amg88sensor
    else:                   
        # Lepton2.5
        import Lepton

#シュミレーター
else:
    # ローカルファイルインポート
    import module

try:
    # 起動中メッセージ表示
    startMsg_disp()

    # 実機
    if setting.mode == 0:
        # センサ初期化
        if setting.sensor == 0:
            # AMG88センサ
            sensor = amg88sensor.Sensor()
        else:
            # Lepton2.5
            sensor = Lepton.Sensor("/dev/spidev0.0")

        # カメラ初期化
        if setting.face_detect == 0:
            # 顔検知OFF
            camera = pygame_camera.Camera(setting.resolution_width, setting.resolution_height, setting.debug)
        else:
            # 顔検知ON
            camera = raspicamera.Camera(setting.resolution_width, setting.resolution_height, setting.debug)

    # Sim
    else:
        print('start dispsim ---')

 
    # 実機/Sim 共通
    # ウィンドウ開く
    open_disp()

    # カラーバー画像作成
    colorbar_img = make_colorbar(setting.colorbar_min, setting.colorbar_max,\
                                 setting.colorbar_width, setting.colorbar_height)

    # 実機
    if setting.mode == 0:
        #センサ、カメラスタート
        sensor.start()
        camera.start()

        while True:

            # 時間計測開始
            #t1 = time.time()

            # センサデータ取得
            sensordata = sensor.GetData()
            #print('------ Thermo Data -------')
            #print(*sensordata, sep='\n')
            #print('--------------------------')

            # 自動キャリブレーション Leptonは未調整
            if setting.sensor == 0:
                GetBodyTempData.setOffsetTempData(sensordata)

            # カメラから映像を取得する
            camera_img = camera.capture()

            # 測定
            BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, bodyTemp, face_rect = \
                measure(camera_img, sensordata, BodyTempArray, BodyTempIndex, SeqCount)

            # OpenCV_data → Pygame_data
            if setting.face_detect == 1: #顔検知ON
                camera_img = convert_opencv_img_to_pygame(camera_img)

            # 結果の画像を表示する
            disp_ret = out_disp(camera_img, colorbar_img, msgStr, msgPos, text_bg_color, bodyTemp, sensordata, face_rect)

            # カメラから読み込んだ映像を破棄する
            camera.seek()

            #時間計測終了
            #t2 = time.time()
            #elapsed_time = t2 - t1
            #print(f"経過時間：{elapsed_time}")


            #　出力失敗の場合または閉じるボタン押下の時は終了する
            if disp_ret == False:
                # センサ終了
                sensor.close()
                # カメラ終了
                camera.close()
                exit()
    #シュミレーター
    else:

        while(True):
            #0.1秒のスリープ
            time.sleep(.1)

            #センサから温度データ取得
            sensordata = module.readTemp()

            # 自動キャリブレーション
            GetBodyTempData.setOffsetTempData(sensordata)

            #カメラ画像データ読み取り
            pic = module.readPic()

            # 測定
            BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, bodyTemp, face_rect = \
                measure(pic, sensordata, BodyTempArray, BodyTempIndex, SeqCount)

            # OpenCV_data → Pygame_data
            img = convert_opencv_img_to_pygame(pic)

            # 画像出力
            disp_ret = out_disp(img, colorbar_img, msgStr, msgPos, text_bg_color, bodyTemp, sensordata, face_rect)

            #　出力失敗の場合または閉じるボタン押下の時は終了する
            if disp_ret == False:
                exit()


#’Ctrl+C’を受け付けると終了
except KeyboardInterrupt:
    print("done")

    # 表示したウィンドウを閉じる
    close_disp()

    if setting.mode == 0:
        # センサ終了
        sensor.close()
        # カメラ終了
        camera.close()
