# calc.py : 

import cv2  # face_detect_on のみで使用
import setting
import GetBodyTempData


# 枠色 BGR
COLOR_NONE = [220, 245, 245]
COLOR_WAIT = [255, 255, 0]
COLOR_OK   = [0, 255, 0]
COLOR_NG   = [0, 0, 255]
COLOR_FRAME = [0, 0, 0]
COLOR_TEXT_BACK = [255, 255, 255]

# センサー座標
START_POS = (200, 80)
#END_POS = (480, 400)
END_POS = (440, 420)

# ステータス文字垂直位置オフセット（背景の下端から離す距離）
if setting.mode == 0:
    # 実機
    STATUS_TEXT_OFFSET_Y = 0
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
JUDGE_TEMP = 37.5

#顔検出パラメータ
SCALE_FACTOR = 1.15
MIN_NIGHBORS = 2
MIN_SIZE = (80,80)

# 体温データの平均回数
AVERAGE_COUNT = 4

#顔検出機能ON
if setting.face_detect:
    # 顔検出のための学習元データを読み込む
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# ------------------------------
# 顔サイズチェック
# Input  : rect
#        : sensordata = サーモセンサデータ
# Return : bodyTemp
# ------------------------------
def check_face_size(rect, sensordata):
  if rect[2] < 10 or rect[3] < 10:
    bodyTemp = GetBodyTempData.getTempData2(sensordata, False, None) # センサ温度の補正
  elif rect[2] > 1000 or rect[3] > 1000:
    bodyTemp = GetBodyTempData.getTempData2(sensordata, False, None) # センサ温度の補正
  else:
    bodyTemp = GetBodyTempData.getTempData2(sensordata, True, rect) # 体温取得 ＆ センサ温度の補正

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
    # 顔検出の処理効率化のために、写真の情報量を落とす（モノクロにする）
    grayimg = cv2.cvtColor(camera_img, cv2.COLOR_BGR2GRAY)

    # 顔検出を行う
    facerect = face_cascade.detectMultiScale(grayimg, scaleFactor=SCALE_FACTOR, \
                                             minNeighbors=MIN_NIGHBORS, minSize=MIN_SIZE)

    # ステータスメッセージ初期値
    msgStr = '枠内に顔を合わせてください'
    msgPos = (124, STATUS_TEXT_POS_Y)  # ステータステキスト表示位置
    text_bg_color = COLOR_NONE

    # 表示用体温（平均値未取得時=0）
    bodyTempAve = 0

    # 顔が１つ検出
    if len(facerect) == 1:
        rect = facerect[0]
        #　顔サイズチェック
        bodyTemp = check_face_size(rect, sensordata)

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
            if bodyTempAve >= JUDGE_TEMP:
                msgStr = 'NG  体温異常'
                text_bg_color = COLOR_NG  # status文字列背景色
            else:
                msgStr = 'OK  体温正常'
                text_bg_color = COLOR_OK  # status文字列背景色

            msgPos = STATUS_TEXT_OK_NG_POS  # ステータステキスト表示位置

    # 顔が検出されなかった場合or複数検出された場合
    else:
        GetBodyTempData.getTempData2(sensordata, False, None) # センサ温度の補正
        #計測不可表示
        BodyTempIndex = 0
        SeqCount = 0
        msgStr = '枠内に顔を合わせてください'
        msgPos = (124, STATUS_TEXT_POS_Y)  # ステータステキスト表示位置
        text_bg_color = [255, 255, 255]  # status文字列背景色

    return BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, round(bodyTempAve, 1)


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
    # 温度データから体温取得 第二引数は顔検出結果の有無。
    
    if setting.sensor == 0:
        #8×8センサー
        # 顔検出機能OFFの場合はTrue固定。
        bodyTemp = GetBodyTempData.getTempData(sensordata, True)

        # ステータスメッセージ初期値
        msgStr = '手首の内側を枠に合わせてください'

    else:
        #80×60センサー
        # 顔検出機能OFFの場合はTrue固定。
        bodyTemp = GetBodyTempData.getTempDataLepton(sensordata, True)

        # ステータスメッセージ初期値
        msgStr = '顔を枠に合わせてください'

    msgPos = (80, STATUS_TEXT_POS_Y)
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
        if bodyTempAve >= JUDGE_TEMP:
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
# Return : BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, body_temp
# ------------------------------
def measure(camera_img, sensordata, BodyTempArray, BodyTempIndex, SeqCount):
    #顔検出機能ON
    if setting.face_detect:
        BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, body_temp = \
            face_detect_on(camera_img, sensordata, BodyTempArray, BodyTempIndex, SeqCount)

    # 顔検出機能OFF
    else:
        BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, body_temp = \
            face_detect_off(sensordata, BodyTempArray, BodyTempIndex, SeqCount)

    return BodyTempIndex, SeqCount, msgStr, msgPos, text_bg_color, body_temp


