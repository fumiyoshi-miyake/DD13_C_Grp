import sys
import time
import cv2

import setting
import module
import GetBodyTempData

#from pygame_util import *
from pygame_util import open_disp
from pygame_util import make_colorbar
from pygame_util import convert_opencv_img_to_pygame
from pygame_util import out_disp
from pygame_util import close_disp

from calc import measure
from calc import AVERAGE_COUNT
    

# 初期化
BodyTempArray = [0] * AVERAGE_COUNT
BodyTempIndex = 0
SeqCount = 0

# 実機
if setting.mode == 0:
    import picamera
    import picamera.array
    import adafruit_amg88xx

    # ローカルファイルインポート
    import raspicamera
    import amg88sensor

#シュミレーター
else:
    # ローカルファイルインポート
    import module


try:

    # 実機
    if setting.mode == 0:
        # センサ初期化
        sensor = amg88sensor.InitSensor( setting.debug )

        # カメラ初期化
        camera = raspicamera.InitCamera( setting.resolution_width, setting.resolution_height, setting.debug )
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
        # カメラの画像をリアルタイムで取得するための処理(streamがメモリー上の画像データ)
        with picamera.array.PiRGBArray(camera) as stream:
            while True:

                # 時間計測開始
                #t1 = time.time()

                # センサデータ取得
                sensordata = sensor.pixels
                # 8x8データ表示(2次元配列)
                #print('------ Thermo Data -------')
                #print(*sensordata, sep='\n')
                #print('--------------------------')

                # 自動キャリブレーション
                GetBodyTempData.setOffsetTempData(sensordata)

                # カメラから映像を取得する（OpenCVへ渡すために、各ピクセルの色の並びをBGRの順番にする）
                camera.capture(stream, 'bgr', use_video_port=True)
                camera_img = stream.array.copy()

                # 測定
                BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, bodyTemp = \
                    measure(camera_img, sensordata, BodyTempArray, BodyTempIndex, SeqCount)

                # OpenCV_data → Pygame_data
                img = convert_opencv_img_to_pygame(img)

                # 結果の画像を表示する
                disp_ret = out_disp(img, colorbar_img, msgStr, msgPos, text_bg_color, bodyTemp, sensordata)

                # カメラから読み込んだ映像を破棄する
                stream.seek(0)
                stream.truncate()

                #時間計測終了
                #t2 = time.time()
                #elapsed_time = t2 - t1
                #print(f"経過時間：{elapsed_time}")


                #　出力失敗の場合または閉じるボタン押下の時は終了する
                if disp_ret == False:
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
        # カメラ終了
        camera.close()
        
