import sys
import time
import cv2
#Setting.iniを使うソースはsetting.pyのimport後にimportする
import setting
import module
from dispsim import *

if setting.mode == 0:
    # 実機
    import picamera
    import picamera.array

    # ローカルファイルインポート
    import raspicamera

    #setting.pyで読み込んだiniファイルのデータを取得
    config_ini = setting.config_ini
    aa = int(config_ini['Common']['mode'])

if setting.debug:
  print('start dispsim ---')

# ウィンドウ開く
#実機
if setting.mode == 0:
    open_disp_machine()
#シュミレーター   
else:
    open_disp()

try:
    # 実機
    if setting.mode == 0:
        # カメラ初期化
        camera = raspicamera.InitCamera( setting.debug )

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
                pass
            pass
    #シュミレーター
    else:
        while(True):
            #0.1秒のスリープ
            time.sleep(.1)
            #時間表示
            print(time.time())
            temp = module.readTemp()
            if setting.debug:
                print(temp)

            pic = module.readPic()
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
