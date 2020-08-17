import os
import sys
import time
import configparser
import cv2

if os.path.exists('Setting.ini'):
    config_ini = configparser.ConfigParser()
    config_ini.read('Setting.ini', encoding='utf-8')

    # 0:実機 1:シュミレーター
    mode = int(config_ini['Common']['mode'])

    #デバッグ出力　OFF:0　ON:1
    debug = int(config_ini['Common']['debug'])
else:
    print('Setting.iniがありません')
    mode = 1
    debug = 0

if mode == 0:
    # 実機
    import picamera
    import picamera.array

    # ローカルファイルインポート
    import raspicamera

try:
    # 実機
    if mode == 0:
        # カメラ初期化
        camera = raspicamera.InitCamera( debug )

        # カメラの画像をリアルタイムで取得するための処理(streamがメモリー上の画像データ)
        with picamera.array.PiRGBArray(camera) as stream:
            while True:
                #######################################################################
                ##########        顔検出と画像表示のサンプルコード              #######
                #######################################################################
                # カメラから映像を取得する（OpenCVへ渡すために、各ピクセルの色の並びをBGRの順番にする）
                #camera.capture(stream, 'bgr', use_video_port=True)

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

                # カメラから読み込んだ映像を破棄する
                #stream.seek(0)
                #stream.truncate()

                #1ミリWait(スリープだと画像が表示されない)
                #cv2.waitKey(1)
                #######################################################################
                ##########        サンプルコード終わり                          #######
                #######################################################################
    #シュミレーター
    else:
        while True:
            #1ミリスリープ
            time.sleep(.1)
            #時間表示
            print(time.time())

#’Ctrl+C’を受け付けると終了
except KeyboardInterrupt:
    print("done")

    if mode == 0:
        # 表示したウィンドウを閉じる
        cv2.destroyAllWindows()

        # カメラ終了
        camera.close()
