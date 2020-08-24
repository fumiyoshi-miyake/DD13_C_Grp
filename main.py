import sys
import time
import cv2
#Setting.iniを使うソースはsetting.pyのimport後にimportする
import setting
import module
import GetBodyTempData

from dispsim import *

from thermo_color import make_colorbar
from thermo_color import make_thermograph
from comp_img import comp_thermo

# 枠色 BGR
COLOR_NONE = [220, 245, 245]
COLOR_WAIT = [255, 204, 0]
COLOR_OK   = [51, 255, 102]
COLOR_NG   = [0, 0, 255]
COLOR_FRAME = [0, 0, 0]

# センサー座標
START_POS = (160, 80)
END_POS = (480, 400)

# 文字座標
OK_NG_POS = (160, 70)
TEMP_POS = (480, 390)

#温度OK/NGしきい値
JUDGE_TEMP = 37.5

#顔検出パラメータ
SCALE_FACTOR = 1.15
MIN_NIGHBORS = 2
MIN_SIZE = (80,80)

# 体温データの平均回数
AVERAGE_COUNT = 4




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
    # 実機/Sim 共通
    # カラーバー画像作成
    colorbar_img = make_colorbar(setting.colorbar_min, setting.colorbar_max,\
                                 setting.colorbar_width, setting.colorbar_height)


    # 実機
    if setting.mode == 0:
        # センサ初期化
        sensor = amg88sensor.InitSensor( setting.debug )

        # カメラ初期化
        camera = raspicamera.InitCamera( setting.debug )

        # ウィンドウ開く
        open_disp_machine()

        #顔検出機能ON
        if setting.face_detect:
            # 顔検出のための学習元データを読み込む
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

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


                # 温度データから体温取得 第二引数は顔検出結果の有無。
                # 顔検出機能OFFの場合はTrue固定。
                bodyTemp = GetBodyTempData.getTempData(sensordata, True)


                # カメラから映像を取得する（OpenCVへ渡すために、各ピクセルの色の並びをBGRの順番にする）
                camera.capture(stream, 'bgr', use_video_port=True)               

                #顔検出機能ON
                if setting.face_detect:

                    # 顔検出の処理効率化のために、写真の情報量を落とす（モノクロにする）
                    grayimg = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)

                    # 顔検出を行う
                    facerect = face_cascade.detectMultiScale(grayimg, scaleFactor=SCALE_FACTOR, minNeighbors=MIN_NIGHBORS, minSize=MIN_SIZE)

                    # 顔が検出された場合
                    if len(facerect) > 0:
                        #検出した場所すべてに赤色で枠を描画する
                        for rect in facerect:
                            #人物検出していないまたは顔枠が複数検出
                            if bodyTemp == 0 or len(facerect) > 1:
                                #計測不可表示
                                color = COLOR_NONE
                                BodyTempIndex = 0
                                SeqCount = 0

                            elif SeqCount < AVERAGE_COUNT:
	    	                 # 測定中表示
                                color = COLOR_WAIT
                                cv2.putText(stream.array, 'wait...', (int(rect[0]),rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=2)        
                                SeqCount += 1
                                BodyTempArray[BodyTempIndex] = bodyTemp
                                BodyTempIndex += 1
                                if BodyTempIndex >= AVERAGE_COUNT:
                                    BodyTempIndex = 0
		                 
                            else:
                                BodyTempArray[BodyTempIndex] = bodyTemp
                                BodyTempIndex += 1
                                if BodyTempIndex >= AVERAGE_COUNT:
                                    BodyTempIndex = 0

                                #体温の平均値算出
                                bodyTempAve = sum(BodyTempArray) / AVERAGE_COUNT
                                if bodyTempAve >= JUDGE_TEMP:
                                    #NG表示
                                    color = COLOR_NG
                                    cv2.putText(stream.array, 'NG', (int(rect[0]),rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)    
                                    cv2.putText(stream.array, "{:.1f}".format(bodyTempAve), (rect[0] + rect[2] + 10,rect[1] + rect[3]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness=2)
                                
                                else:
                                    #OK表示
                                    color = COLOR_OK
                                    cv2.putText(stream.array, 'OK', (int(rect[0]),rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)    
                                    cv2.putText(stream.array, "{:.1f}".format(bodyTempAve), (rect[0] + rect[2] + 10,rect[1] + rect[3]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness=2)
                                
                        cv2.rectangle(stream.array, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), color, thickness=2)              
                    cv2.rectangle(stream.array, START_POS, END_POS, COLOR_FRAME, thickness=1)            

                else:
                # 顔検出機能OFFの描画設定###############
                    if bodyTemp == 0:
                        #計測不可表示
                        color = COLOR_NONE
                        BodyTempIndex = 0
                        SeqCount = 0
                    elif SeqCount < AVERAGE_COUNT:
                        # 測定中表示
                        color = COLOR_WAIT
                        cv2.putText(stream.array, 'wait...', OK_NG_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)        
                        SeqCount += 1
                        BodyTempArray[BodyTempIndex] = bodyTemp
                        BodyTempIndex += 1
                        if BodyTempIndex >= AVERAGE_COUNT:
                            BodyTempIndex = 0

                    else:
                        #OK or NG表示
                        BodyTempArray[BodyTempIndex] = bodyTemp
                        BodyTempIndex += 1
                        if BodyTempIndex >= AVERAGE_COUNT:
                            BodyTempIndex = 0

                        #体温の平均値算出
                        bodyTempAve = sum(BodyTempArray) / AVERAGE_COUNT
                        if bodyTempAve >= JUDGE_TEMP:
                            #NG表示
                            color = COLOR_NG
                            cv2.putText(stream.array, 'NG', OK_NG_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)
                            cv2.putText(stream.array, "{:.1f}".format(bodyTempAve), TEMP_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness=2)
                        else:
                            #OK表示
                            color = COLOR_OK
                            cv2.putText(stream.array, 'OK', OK_NG_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)
                            cv2.putText(stream.array, "{:.1f}".format(bodyTempAve), TEMP_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness=2)

                    cv2.rectangle(stream.array, START_POS, END_POS, color, thickness=1)            
                ########################

                # サーモグラフィ画像作成
                thermo_img = make_thermograph(sensordata, setting.colorbar_min, setting.colorbar_max,\
                                              setting.thermo_width, setting.thermo_height)

                # サーモグラフィ画像合成 & 結果の画像を表示する
                disp_ret = dispsim(comp_thermo(stream.array.copy(), colorbar_img, thermo_img, setting.comp_ofst_x, setting.comp_ofst_y))

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
        print('start dispsim ---')

        # ウィンドウ開く
        open_disp_machine()

        #顔検出機能ON
        if setting.face_detect:
            # 顔検出のための学習元データを読み込む
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

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

            # サーモグラフィ画像作成
            thermo_img = make_thermograph(temp, setting.colorbar_min, setting.colorbar_max,\
            #thermo_img = make_thermograph(sensordata4, setting.colorbar_min, setting.colorbar_max,\
                                            setting.thermo_width, setting.thermo_height)

            #温度データ読み取り
            pic = module.readPic()


            #顔検出機能ON
            if setting.face_detect:

                # 顔検出の処理効率化のために、写真の情報量を落とす（モノクロにする）
                grayimg = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)

                # 顔検出を行う
                facerect = face_cascade.detectMultiScale(grayimg, scaleFactor=SCALE_FACTOR, minNeighbors=MIN_NIGHBORS, minSize=MIN_SIZE)

                # 顔が検出された場合
                if len(facerect) > 0:
                    #検出した場所すべてに赤色で枠を描画する
                    for rect in facerect:
                        #人物検出していないまたは顔枠が複数検出
                        if bodyTemp == 0 or len(facerect) > 1:
                            #計測不可表示
                            color = COLOR_NONE
                            BodyTempIndex = 0
                            SeqCount = 0
                        elif SeqCount < AVERAGE_COUNT:
		             # 測定中表示
                            color = COLOR_WAIT
                            cv2.putText(pic, 'wait...', (int(rect[0]),rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)        
                            SeqCount += 1
                            BodyTempArray[BodyTempIndex] = bodyTemp
                            BodyTempIndex += 1
                            if BodyTempIndex >= AVERAGE_COUNT:
                                BodyTempIndex = 0
		                 
                        else:
                            BodyTempArray[BodyTempIndex] = bodyTemp
                            BodyTempIndex += 1
                            if BodyTempIndex >= AVERAGE_COUNT:
                                BodyTempIndex = 0

                            #体温の平均値算出
                            bodyTempAve = sum(BodyTempArray) / AVERAGE_COUNT
                            if bodyTempAve >= JUDGE_TEMP:
                                #NG表示
                                color = COLOR_NG
                                cv2.putText(pic, 'NG', (int(rect[0]), rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)    
                                cv2.putText(pic, "{:.1f}".format(bodyTempAve), (rect[0] + rect[2] + 10,rect[1] + rect[3]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness=2)
                            else:
                                #OK表示
                                color = COLOR_OK
                                cv2.putText(pic, 'OK', (int(rect[0]),rect[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)    
                                cv2.putText(pic, "{:.1f}".format(bodyTempAve), (rect[0] + rect[2] + 10,rect[1] + rect[3]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness=2)

                        cv2.rectangle(pic, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), color, thickness=2)
                        cv2.rectangle(pic, START_POS, END_POS, COLOR_FRAME, thickness=1)            

            else:
                # 顔検出機能OFFの描画設定###############
                if bodyTemp == 0:
                    #計測不可表示
                    color = COLOR_NONE
                    BodyTempIndex = 0
                    SeqCount = 0
                elif SeqCount < AVERAGE_COUNT:
                    # 測定中表示
                    color = COLOR_WAIT
                    cv2.putText(pic, 'wait...', OK_NG_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)        
                    SeqCount += 1
                    BodyTempArray[BodyTempIndex] = bodyTemp
                    BodyTempIndex += 1
                    if BodyTempIndex >= AVERAGE_COUNT:
                        BodyTempIndex = 0

                else:
                    BodyTempArray[BodyTempIndex] = bodyTemp
                    BodyTempIndex += 1
                    if BodyTempIndex >= AVERAGE_COUNT:
                        BodyTempIndex = 0

                    #体温の平均値算出
                    bodyTempAve = sum(BodyTempArray) / AVERAGE_COUNT
                    if bodyTempAve >= JUDGE_TEMP:
                        #NG表示
                        color = COLOR_NG
                        cv2.putText(pic, 'NG', OK_NG_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)
                        cv2.putText(pic, "{:.1f}".format(bodyTempAve), TEMP_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness=2)
                    else:
                        #OK表示
                        color = COLOR_OK
                        cv2.putText(pic, 'OK', OK_NG_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, thickness=3)
                        cv2.putText(pic, "{:.1f}".format(bodyTempAve), TEMP_POS, cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, thickness=2)

                cv2.rectangle(pic, START_POS, END_POS, color, thickness=1)            
                ########################

            # サーモグラフィ画像合成
            comp_thermo(pic, colorbar_img, thermo_img, setting.comp_ofst_x, setting.comp_ofst_y)

            # 画像出力
            disp_ret = dispsim(pic)

            #　出力失敗の場合または閉じるボタン押下の時は終了する
            if disp_ret == False:
                exit()

#’Ctrl+C’を受け付けると終了
except KeyboardInterrupt:
    print("done")

    if setting.mode == 0:
        # 表示したウィンドウを閉じる
        cv2.destroyAllWindows()

        # カメラ終了
        camera.close()
