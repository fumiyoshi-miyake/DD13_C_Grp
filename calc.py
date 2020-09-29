# calc.py : 

import cv2  # face_detect_on のみで使用
import setting
import GetBodyTempData
import pygame_util

# 枠色 RGB
COLOR_NONE = [245, 245, 220]
COLOR_WAIT = [0, 255, 255]
COLOR_OK   = [0, 255, 0]
COLOR_NG   = [255, 0, 0]
COLOR_FRAME = [0, 0, 0]
COLOR_TEXT_BACK = [255, 255, 255]

# センサー座標
START_POS = (200, 80)
#END_POS = (480, 400)
END_POS = (440, 420)

# ステータス文字垂直位置オフセット（背景の下端から離す距離）
if setting.mode == 0:
    # 実機
    STATUS_TEXT_OFFSET_Y = 8
else:
    # Sim
    STATUS_TEXT_OFFSET_Y = 8

# ステータステキスト表示Y座標
STATUS_TEXT_POS_Y = 44 - STATUS_TEXT_OFFSET_Y
# OK/NG 時のステータステキスト表示座標
STATUS_TEXT_OK_NG_POS = (236, STATUS_TEXT_POS_Y)

# ステータステキスト背景座標
#STATUS_START_POS = (72, 39)
#STATUS_END_POS   = (564, 79)
STATUS_START_POS = (72, START_POS[1]-42)
STATUS_END_POS   = (564, START_POS[1]-2)

# ステータステキスト文字色
STATUS_TEXT_COLOR = (0, 0, 0, 0)

# 温度テキスト文字色
TEMP_TEXT_COLOR = (0, 0, 0)

# 温度テキスト背景座標
#TEMP_START_POS = (480, 360)
#TEMP_END_POS   = (550, 396)
TEMP_START_POS = (END_POS[0]+2, END_POS[1]-36)
TEMP_END_POS   = (TEMP_START_POS[0]+70+6, END_POS[1])

# 温度テキスト垂直位置オフセット（背景の下端から離す距離）
TEMP_TEXT_OFFSET_Y = 6
# 温度テキスト座標
#TEMP_POS = (480, 360 - TEMP_TEXT_OFFSET_Y)
TEMP_POS = (TEMP_START_POS[0]+2, TEMP_END_POS[1] - TEMP_TEXT_OFFSET_Y)

#温度OK/NGしきい値
_judge_temp = setting.judge_temp

#顔検出パラメータ
SCALE_FACTOR = 1.1
MIN_NIGHBORS = 3
MIN_SIZE = (40,40)

# 体温データの平均回数
AVERAGE_COUNT = 4

#顔検出機能ON
#if setting.face_detect:
# 顔検出のための学習元データを読み込む
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier('cascade.xml')


# ------------------------------
# 複数顔から画面中央に一番近い顔を選択
# Input  : face_rect = 顔検出データ（配列）
# Return : rect
# ------------------------------
def face_select(face_rect):
    num = len(face_rect)
    minPos = 420
    index = 0
    for i in range(num):
        cx = face_rect[i][0] + face_rect[i][2] / 2
        cy = face_rect[i][1] + face_rect[i][3] / 2
        if minPos > abs(240 - cx) + abs(180 - cy):
            minPos = abs(240 - cx) + abs(180 - cy)
            index = i

    return face_rect[index]

# ------------------------------
# 顔枠が矩形内に収まっているか判定
# Input  : face_rect = 顔枠
# Return : 判定結果
# ------------------------------
def check_face_pos(face_rect):
    # 
    startx = face_rect[0]
    starty = face_rect[1]
    endx = face_rect[0] + face_rect[2]
    endy = face_rect[1] + face_rect[3]

    if startx > 0 and starty > 0 and endx < 480 and endy < 360:
        return True
    return False

# ------------------------------
# 顔サイズチェック
# Input  : rect
#        : sensordata = サーモセンサデータ
# Return : bodyTemp
# ------------------------------
def check_face_size(rect, sensordata):
  if rect[2] < 70 or rect[3] < 70:
    bodyTemp = GetBodyTempData.getTempDataFaceDetOn(sensordata, False, None) # センサ温度の補正
  elif rect[2] > 500 or rect[3] > 500:
    bodyTemp = GetBodyTempData.getTempDataFaceDetOn(sensordata, False, None) # センサ温度の補正
  else:
    bodyTemp = GetBodyTempData.getTempDataFaceDetOn(sensordata, True, rect) # 体温取得 ＆ センサ温度の補正

  return bodyTemp


# ------------------------------
# 顔検出On
# Input  : camera_img    = カメラ画像データ
#        : sensordata    = サーモセンサデータ
#        : BodyTempArray = 体温データ
#        : BodyTempIndex, SeqCount,
# Return : BodyTempIndex, SeqCount,
#        : msgStr        = ステータス表示文字列
#        : msgPos        = ステータス表示文字列位置
#        : text_bg_color = 文字列背景色
# ------------------------------
def face_detect_on(camera_img, sensordata, BodyTempArray, BodyTempIndex, SeqCount):
    global _judge_temp
    
    # 高さ・幅・色を取得
    height, width, color = camera_img.shape
    # 顔検出の処理効率化のために、写真をリサイズ
    dst = cv2.resize(camera_img, (int(width / 2), int(height / 2))) 
    # 顔検出の処理効率化のために、写真の情報量を落とす（モノクロにする）
    grayimg = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    # # 顔検出の処理効率化のために、写真の情報量を落とす（モノクロにする）
    # grayimg = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)

    # 顔検出を行う
    facerect = face_cascade.detectMultiScale(grayimg, scaleFactor=SCALE_FACTOR, \
                                             minNeighbors=MIN_NIGHBORS, minSize=MIN_SIZE)
    # # 縮小前のサイズに戻す
    facerect = facerect * 2 

    # ステータスメッセージ初期値
    msgStr = '体温を測定します'
    msgPos = (204, STATUS_TEXT_POS_Y)  # ステータステキスト表示位置
    text_bg_color = COLOR_NONE

    # 表示用体温（平均値未取得時=0）
    bodyTempAve = 0

    face_rect = [0,0,0,0]

    # 顔が複数ある場合は、画面中央に近い１つにする
    if len(facerect) == 0:
        face_pos_judge = False
    else:
        if len(facerect) == 1:
            face_rect = facerect[0]
        else:
            face_rect = face_select(facerect)
        
        #顔枠がセンサー範囲に収まっているか判定 
        face_pos_judge = check_face_pos(face_rect)



    # 体温測定できた顔があるか
    if len(facerect) >= 1:
        #　顔サイズチェック
        bodyTemp = check_face_size(face_rect, sensordata)

        #計測不可表示(顔をカメラに近づけてください又は顔をカメラから離してください)
        if bodyTemp == 0:
            BodyTempIndex = 0
            SeqCount = 0
            text_bg_color = [255, 255, 255]  # status文字列背景色
        # 測定中表示
        elif SeqCount < AVERAGE_COUNT:
            text_bg_color = COLOR_WAIT  # status文字列背景色
            msgStr = '計測中...'
            msgPos = (270, STATUS_TEXT_POS_Y)  # ステータステキスト表示位置
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
            if bodyTempAve >= _judge_temp:
                msgStr = 'NG  体温異常'
                text_bg_color = COLOR_NG  # status文字列背景色
            else:
                msgStr = 'OK  体温正常'
                text_bg_color = COLOR_OK  # status文字列背景色

            msgPos = STATUS_TEXT_OK_NG_POS  # ステータステキスト表示位置

    # 顔が検出されなかった場合or複数検出された場合
    else:
        GetBodyTempData.getTempDataFaceDetOn(sensordata, False, face_rect) # センサ温度の補正
        #計測不可表示
        BodyTempIndex = 0
        SeqCount = 0
        msgStr = '体温を測定します'
        msgPos = (204, STATUS_TEXT_POS_Y)  # ステータステキスト表示位置
        text_bg_color = [255, 255, 255]  # status文字列背景色

    return BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, round(bodyTempAve, 1), face_rect


# ------------------------------
# 顔検出Off
# Input  : sensordata    = サーモセンサデータ
#        : BodyTempArray = 体温データ
#        : BodyTempIndex, SeqCount,
# Return : BodyTempIndex, SeqCount,
#        : msgStr        = ステータス表示文字列
#        : msgPos        = ステータス表示文字列位置
#        : text_bg_color = 文字列背景色
#        : bodyTempAve   = 平均体温
# ------------------------------
def face_detect_off(sensordata, BodyTempArray, BodyTempIndex, SeqCount):
    global _judge_temp
    
    # 温度データから体温取得
    bodyTemp = GetBodyTempData.getTempDataFaceDetOff(sensordata)
    
    # ステータスメッセージ初期値
    if setting.sensor == 0 and setting.measure_mode == 1:
        msgStr = '手首の内側を枠に合わせてください'
        msgPos = (80, STATUS_TEXT_POS_Y)
    else:
        msgStr = '顔を枠に合わせてください'
        msgPos = (137, STATUS_TEXT_POS_Y)

    text_bg_color = COLOR_NONE
    
    # 表示用体温（平均値未取得時=0）
    bodyTempAve = 0

    if bodyTemp == 0:
        #計測不可表示
        text_bg_color = COLOR_NONE
        BodyTempIndex = 0
        SeqCount = 0
    elif SeqCount < AVERAGE_COUNT:
        # 測定中表示
        text_bg_color = COLOR_WAIT
        msgStr = '計測中...'
        msgPos = (270, STATUS_TEXT_POS_Y)  # ステータステキスト表示位置

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
        if bodyTempAve >= _judge_temp:
            msgStr = 'NG  体温異常'
            text_bg_color = COLOR_NG  # status文字列背景色
        else:
            msgStr = 'OK  体温正常'
            text_bg_color = COLOR_OK  # status文字列背景色

        msgPos = STATUS_TEXT_OK_NG_POS  # ステータステキスト表示位置

    # 体温は小数第2位を四捨五入
    return BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, round(bodyTempAve, 1)


# ------------------------------
# 測定
# Input  : camera_img    = カメラ画像データ
#        : sensordata    = サーモセンサデータ
#        : BodyTempArray = 体温データ
#        : BodyTempIndex, SeqCount,
# Return : BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, body_temp, face_rect
# ------------------------------
def measure(camera_img, sensordata, BodyTempArray, BodyTempIndex, SeqCount, face_detect, threshold):
    global _judge_temp
    _judge_temp = threshold
    #顔検出機能ON
    if face_detect == 1:
        BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, body_temp, face_rect = \
            face_detect_on(camera_img, sensordata, BodyTempArray, BodyTempIndex, SeqCount)

    # 顔検出機能OFF
    else:
        BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, body_temp = \
            face_detect_off(sensordata, BodyTempArray, BodyTempIndex, SeqCount)
        face_rect = [0, 0, 0, 0]

    return BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, body_temp, face_rect


