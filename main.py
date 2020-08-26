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
from text_jp import putJapaneseText

# 枠色 BGR
COLOR_NONE = [220, 245, 245]
COLOR_WAIT = [255, 0, 0]
COLOR_OK   = [0, 255, 0]
COLOR_NG   = [0, 0, 255]
COLOR_FRAME = [0, 0, 0]

# センサー座標
START_POS = (160, 80)
#END_POS = (480, 400)
END_POS = (480, 420)

# 文字座標
OK_NG_POS = (160, 70)
TEMP_POS = (480, 390)

#COLOR_TEXT_BACK = [255, 255, 255]
# ステータステキスト背景座標
#STATUS_START_POS = (160, 40)
STATUS_START_POS = (102, 39)
#STATUS_END_POS = (480, 80)
STATUS_END_POS = (534, 79)

# 温度テキスト背景座標
#TEMP_START_POS = (480, 360)
TEMP_START_POS = (480, 360)
#TEMP_END_POS = (550, 390)
TEMP_END_POS = (550, 396)

#温度OK/NGしきい値
JUDGE_TEMP = 37.5

#顔検出パラメータ
SCALE_FACTOR = 1.15
MIN_NIGHBORS = 2
MIN_SIZE = (80,80)

# 体温データの平均回数
AVERAGE_COUNT = 4




# 顔サイズチェック
# Input  : rect_2, rect_3
# Return : bodyTemp
def check_face_size(rect_2, rect_3):
  if rect_2 < 200 or rect_3 < 320:
    bodyTemp = GetBodyTempData.getTempData2(sensordata, False, None) # センサ温度の補正
  elif rect_2 > 400 or rect_3 > 420:
    bodyTemp = GetBodyTempData.getTempData2(sensordata, False, None) # センサ温度の補正
  else:
    bodyTemp = GetBodyTempData.getTempData2(sensordata, True, rect) # 体温取得 ＆ センサ温度の補正

  return bodyTemp


# 体温描画
# Input : camera_img = カメラ画像データ
#       : body_temp  = 体温
#       : text_bg_color = status文字列背景 
def draw_temp(camera_img, body_temp, text_bg_color):
  cv2.rectangle(camera_img, TEMP_START_POS, TEMP_END_POS, text_bg_color, thickness=-1)
  cv2.putText(camera_img, "{:.1f}".format(body_temp), TEMP_POS,\
              cv2.FONT_HERSHEY_SIMPLEX, 1.0, COLOR_FRAME, thickness=2)

  return



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
                msgStr = ''

                # 時間計測開始
                #t1 = time.time()

                # センサデータ取得
                sensordata = sensor.pixels
                # 8x8データ表示(2次元配列)
                #print('------ Thermo Data -------')
                #print(*sensordata, sep='\n')
                #print('--------------------------')

                # カメラから映像を取得する（OpenCVへ渡すために、各ピクセルの色の並びをBGRの順番にする）
                camera.capture(stream, 'bgr', use_video_port=True)
                camera_img = stream.array.copy()

                # ステータスメッセージ表示用初期値
                msgColor = (0, 0, 0, 0)
                msgPos = (124, 44)

                #顔検出機能ON
                if setting.face_detect:

                    # 顔検出の処理効率化のために、写真の情報量を落とす（モノクロにする）
                    grayimg = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)

                    # 顔検出を行う
                    facerect = face_cascade.detectMultiScale(grayimg, scaleFactor=SCALE_FACTOR, \
                                                             minNeighbors=MIN_NIGHBORS, minSize=MIN_SIZE)

                    # ステータスメッセージ初期値
                    msgStr = '枠内に顔を合わせてください'

                    # 顔が１つ検出
                    if len(facerect) == 1:
                        rect = facerect[0]
                        #　顔サイズチェック
                        bodyTemp = check_face_size(rect[2], rect[3])

                        #計測不可表示(顔をカメラに近づけてください又は顔をカメラから離してください)
                        if bodyTemp == 0:
                            BodyTempIndex = 0
                            SeqCount = 0
                            COLOR_TEXT_BACK = [255, 255, 255]  # status文字列背景色
                        # 測定中表示
                        elif SeqCount < AVERAGE_COUNT:
                            COLOR_TEXT_BACK = COLOR_WAIT  # status文字列背景色
                            msgStr = '計測中...'
                            msgPos = (270, 44)
                            SeqCount += 1
                            BodyTempArray[BodyTempIndex] = bodyTemp
                            BodyTempIndex += 1
                            if BodyTempIndex >= AVERAGE_COUNT:
                                BodyTempIndex = 0
                        # 体温表示
                        else:
                            BodyTempArray[BodyTempIndex] = bodyTemp
                            BodyTempIndex += 1
                            if BodyTempIndex >= AVERAGE_COUNT:
                                BodyTempIndex = 0

                            #体温の平均値算出
                            bodyTempAve = sum(BodyTempArray) / AVERAGE_COUNT
                            if bodyTempAve >= JUDGE_TEMP:
                                msgStr = 'NG  体温異常'
                                COLOR_TEXT_BACK = COLOR_NG  # status文字列背景色

                            else:
                                msgStr = 'OK  体温正常'
                                COLOR_TEXT_BACK = COLOR_OK  # status文字列背景色

                            msgColor = (0, 0, 0, 0)
                            msgPos = (236, 44)

                            # 体温描画
                            draw_temp(camera_img, bodyTempAve, COLOR_TEXT_BACK)

                            
                    # 顔が検出されなかった場合or複数検出された場合
                    else:
                        GetBodyTempData.getTempData2(sensordata, False, None) # センサ温度の補正
                        #計測不可表示
                        BodyTempIndex = 0
                        SeqCount = 0
                        msgStr = '枠内に顔を合わせてください'
                        msgPos = (124, 44)
                        COLOR_TEXT_BACK = [255, 255, 255]  # status文字列背景色

                else:
                    # 顔検出機能OFFの描画設定###############
                    # 温度データから体温取得 第二引数は顔検出結果の有無。
                    # 顔検出機能OFFの場合はTrue固定。
                    bodyTemp = GetBodyTempData.getTempData(sensordata, True)

                    # ステータスメッセージ初期値
                    msgStr = ''

                    if bodyTemp == 0:
                        #計測不可表示
                        COLOR_TEXT_BACK = COLOR_NONE
                        BodyTempIndex = 0
                        SeqCount = 0
                    elif SeqCount < AVERAGE_COUNT:
                        # 測定中表示
                        COLOR_TEXT_BACK = COLOR_WAIT
                        msgStr = '計測中...'
                        msgPos = (270, 44)

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
                            msgStr = 'NG  体温異常'
                            COLOR_TEXT_BACK = COLOR_NG  # status文字列背景色
                        else:
                            msgStr = 'OK  体温正常'
                            COLOR_TEXT_BACK = COLOR_OK  # status文字列背景色

                        msgColor = (0, 0, 0, 0)
                        msgPos = (236, 44)

                        # 体温描画
                        draw_temp(camera_img, bodyTempAve, COLOR_TEXT_BACK)

                # status文字列背景描画
                cv2.rectangle(camera_img, STATUS_START_POS, STATUS_END_POS, COLOR_TEXT_BACK, thickness=-1)
                        
                # センサ範囲矩形描画
                cv2.rectangle(camera_img, START_POS, END_POS, COLOR_NONE, thickness=2)            

                ########################



                # サーモグラフィ画像作成
                thermo_img = make_thermograph(sensordata, setting.colorbar_min, setting.colorbar_max,\
                                              setting.thermo_width, setting.thermo_height)

                # サーモグラフィ画像合成
                img = comp_thermo(camera_img, colorbar_img, thermo_img,\
                                  setting.comp_ofst_x, setting.comp_ofst_y)

                #msg(日本語文字)合成
                if msgStr != '':
                    img = putJapaneseText(img, msgStr, msgPos, msgColor)

                # 結果の画像を表示する
                disp_ret = dispsim(img)

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
            sensordata = module.readTemp()

            # 温度データから体温取得 第二引数は顔検出結果の有無。
            # 顔検出機能OFFの場合はTrue固定。
            bodyTemp = GetBodyTempData.getTempData(sensordata, True)
            if setting.debug:
                print(bodyTemp)


            #カメラ画像データ読み取り
            pic = module.readPic()

            # ステータスメッセージ表示用初期値
            msgColor = (0, 0, 0, 0)
            msgPos = (124, 44)


            #顔検出機能ON
            if setting.face_detect:

                # 顔検出の処理効率化のために、写真の情報量を落とす（モノクロにする）
                grayimg = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)

                # 顔検出を行う
                facerect = face_cascade.detectMultiScale(grayimg, scaleFactor=SCALE_FACTOR,\
                                                         minNeighbors=MIN_NIGHBORS, minSize=MIN_SIZE)

                # ステータスメッセージ初期値
                msgStr = '枠内に顔を合わせてください'

                # 顔が検出された場合
                if len(facerect) > 0:
                    #検出した場所すべてに赤色で枠を描画する
                    for rect in facerect:
                        #人物検出していないまたは顔枠が複数検出
                        if bodyTemp == 0 or len(facerect) > 1:
                            #計測不可表示
                            BodyTempIndex = 0
                            SeqCount = 0
                        elif SeqCount < AVERAGE_COUNT:
                            # 測定中表示
                            COLOR_TEXT_BACK = COLOR_WAIT  # status文字列背景色
                            msgStr = '計測中...'
                            msgPos = (270, 44)
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
                                msgStr = 'NG  体温異常'
                                COLOR_TEXT_BACK = COLOR_NG  # status文字列背景色
                            else:
                                msgStr = 'OK  体温正常'
                                COLOR_TEXT_BACK = COLOR_OK  # status文字列背景色

                            msgColor = (0, 0, 0, 0)
                            msgPos = (236, 44)
                            # 体温描画
                            draw_temp(pic, bodyTempAve, COLOR_TEXT_BACK)
                            
                        cv2.rectangle(pic, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]),\
                                      COLOR_TEXT_BACK, thickness=2)

            else:
                # 顔検出機能OFFの描画設定###############

                # ステータスメッセージ初期値
                msgStr = ''

                if bodyTemp == 0:
                    #計測不可表示
                    BodyTempIndex = 0
                    SeqCount = 0
                elif SeqCount < AVERAGE_COUNT:
                    # 測定中表示
                    COLOR_TEXT_BACK = COLOR_WAIT  # status文字列背景色
                    msgStr = '計測中...'
                    msgPos = (270, 44)

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
                        msgStr = 'NG  体温異常'
                        COLOR_TEXT_BACK = COLOR_NG  # status文字列背景色
                    else:
                        msgStr = 'OK  体温正常'
                        COLOR_TEXT_BACK = COLOR_OK  # status文字列背景色

                    msgColor = (0, 0, 0, 0)
                    msgPos = (236, 44)
                    # 体温描画
                    draw_temp(pic, bodyTempAve, COLOR_TEXT_BACK)

                ########################
                
            # status文字列背景描画
            cv2.rectangle(pic, STATUS_START_POS, STATUS_END_POS, COLOR_TEXT_BACK, thickness=-1)
                        
            # センサ範囲矩形描画
            cv2.rectangle(pic, START_POS, END_POS, COLOR_NONE, thickness=1)            

            # サーモグラフィ画像作成
            thermo_img = make_thermograph(sensordata, setting.colorbar_min, setting.colorbar_max,\
                                          setting.thermo_width, setting.thermo_height)

            # サーモグラフィ画像合成
            img = comp_thermo(pic, colorbar_img, thermo_img, setting.comp_ofst_x, setting.comp_ofst_y)

            #msg(日本語文字)合成
            if msgStr != '':
                img = putJapaneseText(img, msgStr, msgPos, msgColor)


            # 画像出力
            disp_ret = dispsim(img)

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
