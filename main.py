import sys
import time
import cv2
#Setting.iniを使うソースはsetting.pyのimport後にimportする
import setting
import module
import GetBodyTempData

from dispsim import *

# 枠色
COLOR_NONE = [0, 0, 0]
COLOR_OK   = [51, 255, 102]
COLOR_NG   = [0, 0, 255]

# センサー座標
START_POS = (160, 80)
END_POS = (480, 400)

# 文字座標
OK_NG_POS = (300, 70)
TEMP_POS = (480, 390)

#温度OK/NGしきい値


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
        camera = raspicamera.InitCamera( setting.debug )

        # ウィンドウ開く
        open_disp_machine()

        # カメラの画像をリアルタイムで取得するための処理(streamがメモリー上の画像データ)
        with picamera.array.PiRGBArray(camera) as stream:
            while True:
                #######################################################################
                ##########        顔検出と画像表示のサンプルコード              #######
                #######################################################################
                # センサデータ取得
                sensordata = sensor.pixels
                #if setting.debug:
                #    # 8x8データ表示(2次元配列)
                #    print('------ Thermo Data -------')
                #    print(*sensordata, sep='\n')
                #    print('--------------------------')



                # 温度データから体温取得 第二引数は顔検出結果の有無。
                # 顔検出機能OFFの場合はTrue固定。
                bodyTemp = GetBodyTempData.getTempData(sensordata, True)


                # カメラから映像を取得する（OpenCVへ渡すために、各ピクセルの色の並びをBGRの順番にする）
                camera.capture(stream, 'bgr', use_video_port=True)

                # 顔検出の処理効率化のために、写真の情報量を落とす（モノクロにする）
                #grayimg = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)

                # 顔検出のための学習元データを読み込む
                #face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                # 顔検出を行う
                #facerect = face_cascade.detectMultiScale(grayimg, scaleFactor=1.2, minNeighbors=2, minSize=(100, 100))

                # 顔が検出された場合
                #if len(facerect) > 0:
                    # 検出した場所すべてに赤色で枠を描画する
                #    for rect in facerect:
                #        cv2.rectangle(stream.array, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0, 255), thickness=3)

                # 結果の画像を表示する
                #cv2.imshow('camera', stream.array)

                # 顔検出機能OFFの描画設定###############
                if bodyTemp == 0:
                    #計測不可表示
                    color = COLOR_NONE
                elif bodyTemp >= 35.5:
                    #NG表示
                    color = COLOR_NG
                    cv2.putText(stream.array, 'NG', OK_NG_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)
                    cv2.putText(stream.array, "{:.1f}".format(bodyTemp), TEMP_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness=2)
                else:
                    #OK表示
                    color = COLOR_OK
                    cv2.putText(stream.array, 'OK', OK_NG_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)
                    cv2.putText(stream.array, "{:.1f}".format(bodyTemp), TEMP_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness=2)

                cv2.rectangle(stream.array, START_POS, END_POS, color, thickness=1)            
                ########################



                # カメラから読み込んだ映像を破棄する
                stream.seek(0)
                stream.truncate()

                #1ミリWait(スリープだと画像が表示されない)
                cv2.waitKey(1)
                #######################################################################
                ##########        サンプルコード終わり                          #######
                #######################################################################
    #シュミレーター
    else:
        print('start dispsim ---')

        # ウィンドウ開く
        open_disp()

        while(True):
            #0.1秒のスリープ
            time.sleep(.1)
            #時間表示
            #print(time.time())

            #センサから温度データ取得
            temp = module.readTemp()

            # 温度データから体温取得 第二引数は顔検出結果の有無。
            # 顔検出機能OFFの場合はTrue固定。
            bodyTemp = GetBodyTempData.getTempData(temp, True)
            if setting.debug:
                print(bodyTemp)

            pic = module.readPic()


            # 顔検出機能OFFの描画設定###############
            if bodyTemp == 0:
                #計測不可表示
                color = COLOR_NONE
            elif bodyTemp >= 37.5:
                #NG表示
                color = COLOR_NG
                cv2.putText(pic, 'NG', OK_NG_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)
                cv2.putText(pic, "{:.1f}".format(bodyTemp), TEMP_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness=2)
            else:
                #OK表示
                color = COLOR_OK
                cv2.putText(pic, 'OK', OK_NG_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)
                cv2.putText(pic, "{:.1f}".format(bodyTemp), TEMP_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness=2)

            cv2.rectangle(pic, START_POS, END_POS, color, thickness=1)            
            ########################
            
            if setting.debug:
            #画像出力
                dispsim(pic)

#’Ctrl+C’を受け付けると終了
except KeyboardInterrupt:
    print("done")

    if setting.mode == 0:
        # 表示したウィンドウを閉じる
        cv2.destroyAllWindows()

        # カメラ終了
        camera.close()
