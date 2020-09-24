import numpy as np
import module
import setting

# 温度測定判定で使用する温度しきい値
TEMPERATURE_TH = 34.0

# 体温オフセット値変更しきい値
CHNAGE_OFFSET_TEMP_MAX = 29.375
CHNAGE_OFFSET_TEMP_MIN = 24.875


if setting.sensor == 0:
    # 温度測定判定で使用する温度しきい値以上のデータ数のしきい値
    AVERAGE_COUNT_TH = 8
    # 測定手法（0:平均値, 1:最大値）
    MEASUREMENT_METHOD = 0

    # センサー有効画素領域
    SENSOR_VALID_START_LINE_X = 1
    SENSOR_VALID_END_LINE_X = 6
    SENSOR_VALID_START_LINE_Y = 1
    SENSOR_VALID_END_LINE_Y = 6

    # 測定距離判定チェック領域
    DIS_CHK_AREA_START_LINE_X = 0
    DIS_CHK_AREA_END_LINE_X = 7
    DIS_CHK_AREA_START_LINE_Y = 1
    DIS_CHK_AREA_END_LINE_Y = 6
    
    # 測定距離判定TH TH以上のとき測定しない MAX=24
    DIS_CHK_AREA_TH = 20

    # 体温のオフセット値(この値は周辺温度により変動する)
    offset_temp = 5

    # キャリブレーション実行判定　最高温度と最低温度の差
    CHANGE_OFFSET_TEMP = 3.0

    # 遠い時の温度補正するかどうかのしきい値
    DIS_ADJ_FAR_TH = 8
    # 近い時の温度補正するかどうかのしきい値
    DIS_ADJ_NEAR_TH = 16

    # センサ1画素あたりのカメラ画素
    SENSOR_TO_CAMERA_PIXCEL = 80

    # 顔サイズ別オフセット値
    SIZE_OFFSET_400 = -2
    SIZE_OFFSET_350 = -1.5
    SIZE_OFFSET_300 = -1
    SIZE_OFFSET_250 = -0.5
    SIZE_OFFSET_200 = 0
    SIZE_OFFSET_170 = 0.2
    SIZE_OFFSET_150 = 0.3
    SIZE_OFFSET_130 = 0.4
    SIZE_OFFSET_100 = 0.8
    SIZE_OFFSET_ELSE = 1.2

    # 顔測定
    if setting.measure_mode == 0:
        # 周辺温度が最低の時のオフセット値
        MIN_OFFSET_TEMP = 4.5
        # 周辺温度が最高の時のオフセット値
        MAX_OFFSET_TEMP = 3.0

    # 手首測定
    else:
        # 周辺温度が最低の時のオフセット値
        MIN_OFFSET_TEMP = 4.9
        # 周辺温度が最高の時のオフセット値
        MAX_OFFSET_TEMP = 3.525   

else:
##### Lepton2.5
    # 温度測定判定で使用する温度しきい値以上のデータ数のしきい値
    AVERAGE_COUNT_TH = 350
    # 測定手法（0:平均値, 1:最大値）
    MEASUREMENT_METHOD = 1

    # センサー有効画素領域
    SENSOR_VALID_START_LINE_X = 25
    SENSOR_VALID_END_LINE_X = 56
    SENSOR_VALID_START_LINE_Y = 10
    SENSOR_VALID_END_LINE_Y = 41

    # 測定距離判定チェック領域
    DIS_CHK_AREA_START_LINE_X = 20
    DIS_CHK_AREA_END_LINE_X = 61
    DIS_CHK_AREA_START_LINE_Y = 10
    DIS_CHK_AREA_END_LINE_Y = 41

    # 測定距離判定TH TH以上のとき測定しない MAX=1200
    DIS_CHK_AREA_TH = 850

    # 体温のオフセット値(Leptonは未調整なので固定)
    offset_temp = 2.0

    # キャリブレーション実行判定　最高温度と最低温度の差
    CHANGE_OFFSET_TEMP = 2.0

    # センサ1画素あたりのカメラ画素
    SENSOR_TO_CAMERA_PIXCEL = 8

    # 周辺温度が最低の時のオフセット値
    MIN_OFFSET_TEMP = 2.0
    # 周辺温度が最高の時のオフセット値
    MAX_OFFSET_TEMP = 2.0

    # 遠い時の温度補正するかどうかのしきい値
    DIS_ADJ_FAR_TH = 400
    # 近い時の温度補正するかどうかのしきい値
    DIS_ADJ_NEAR_TH = 850

    # 顔サイズ別オフセット値
    SIZE_OFFSET_400 = -2
    SIZE_OFFSET_350 = -1.5
    SIZE_OFFSET_300 = -1
    SIZE_OFFSET_250 = -0.5
    SIZE_OFFSET_200 = 0
    SIZE_OFFSET_170 = 0.2
    SIZE_OFFSET_150 = 0.3
    SIZE_OFFSET_130 = 0.4
    SIZE_OFFSET_100 = 0.8
    SIZE_OFFSET_ELSE = 1.2


# ------------------------------
# キャリブレーション 体温オフセット値チェック
# ------------------------------
def setOffsetTempData(inTemp):
    global offset_temp

    # 左上、右上、左下、右下の4隅から算出
    arr = [inTemp[0][0], inTemp[0][module.col_count-1], inTemp[module.row_count-1][0], inTemp[module.row_count -1][module.col_count-1]]

   # NumPy配列 ndarrayに変換
    tmp = np.array(arr)

    maxTemp = tmp.max()
    minTemp = tmp.min()
    decideTemp = ( maxTemp + minTemp ) / 2

    # 最高温度と最低温度の差がしきい値以下か
    if (maxTemp - minTemp <= CHANGE_OFFSET_TEMP) and \
        (decideTemp <= CHNAGE_OFFSET_TEMP_MAX) and \
        (decideTemp >= CHNAGE_OFFSET_TEMP_MIN):
        
        offset_temp = MIN_OFFSET_TEMP - (decideTemp - CHNAGE_OFFSET_TEMP_MIN) *\
         (MIN_OFFSET_TEMP - MAX_OFFSET_TEMP) / (CHNAGE_OFFSET_TEMP_MAX - CHNAGE_OFFSET_TEMP_MIN)

    return

# ------------------------------
# 温度データ取得 顔検出OFFモード
# ------------------------------
def getTempDataFaceDetOff(inTemp):
    global offset_temp
    outTemp = 0
    sumTemp = 0
    countTemp = 0
    maxTemp = 0
    countDisCheck = 0

    # センサ解像度分ループ
    for i in range(module.row_count):
        for j in range(module.col_count):
            #オフセットは全データに加算
            inTemp[i][j] += offset_temp
            
            # センサの有効範囲チェック
            if j > SENSOR_VALID_START_LINE_X and j < SENSOR_VALID_END_LINE_X and \
               i > SENSOR_VALID_START_LINE_Y and i < SENSOR_VALID_END_LINE_Y and \
               TEMPERATURE_TH <= inTemp[i][j]:
                countTemp += 1
                sumTemp += inTemp[i][j]
                if maxTemp < inTemp[i][j]:
                    maxTemp = inTemp[i][j]

            # 距離判定用面積チェック
            if j > DIS_CHK_AREA_START_LINE_X and j < DIS_CHK_AREA_END_LINE_X and \
               i > DIS_CHK_AREA_START_LINE_Y and i < DIS_CHK_AREA_END_LINE_Y and \
               TEMPERATURE_TH <= inTemp[i][j]:
                countDisCheck += 1


    # 距離チェック 面積がTH以上は近すぎと判断して測定しない
    if countDisCheck >= DIS_CHK_AREA_TH:
        return 0

    # しきい値以上の温度データが得られたら、温度データを返却する
    if countTemp >= AVERAGE_COUNT_TH:
       # 平均値出力
       if MEASUREMENT_METHOD == 0:
          outTemp = sumTemp / countTemp

       # 最大値出力
       else:
          outTemp = maxTemp
          
       # 距離によるOFFSET値 （注意：サーモ用データには反映していない）
       if countTemp < DIS_ADJ_FAR_TH:
           outTemp += 0.5
       elif countTemp > DIS_ADJ_NEAR_TH:
           outTemp -= 0.5
           
           
    return outTemp

# ------------------------------
# 温度データ取得 顔検出ONモード
# ------------------------------
def getTempDataFaceDetOn(inTemp, isDetFace, rect):
    outTemp = 0

    offset = offset_temp
    # 顔サイズによる温度オフセット(できるだけ細かく調整)
    if rect[2] > 400:
        offset += SIZE_OFFSET_400
    elif rect[2] > 350:
        offset += SIZE_OFFSET_350
    elif rect[2] > 300:
        offset += SIZE_OFFSET_300
    elif rect[2] > 250:
        offset += SIZE_OFFSET_250
    elif rect[2] > 200:
        offset += SIZE_OFFSET_200
    elif rect[2] > 170:
        offset += SIZE_OFFSET_170
    elif rect[2] > 150:
        offset += SIZE_OFFSET_150
    elif rect[2] > 130:
        offset += SIZE_OFFSET_130
    elif rect[2] > 100:
        offset += SIZE_OFFSET_100
    elif rect[2] == 0:
        offset += 0    
    else:
        offset += SIZE_OFFSET_ELSE


    # センサ解像度分ループ
    for i in range(module.row_count):
        for j in range(module.col_count):
            #オフセットは全データに加算
            inTemp[i][j] += offset

    # 人物検出していない場合は0（無効値）を返す
    if isDetFace == False:
       return 0

    #枠の領域計算(pixel)
    startX = rect[0]
    endX   = rect[0] + rect[2]
    startY = rect[1]
    endY2  = rect[1] + rect[3]

    #枠の領域(pixel)から温度データ配列のインデックスに変換
    x1 = int(startX / SENSOR_TO_CAMERA_PIXCEL)
    x2 = int(endX   / SENSOR_TO_CAMERA_PIXCEL) + 1
    y1 = int(startY / SENSOR_TO_CAMERA_PIXCEL) + 1
    y2 = int(endY2  / SENSOR_TO_CAMERA_PIXCEL) + 1 + 1

    # NumPy配列 ndarrayに変換
    tmp = np.array(inTemp)

    # 温度測定に必要な要素を抽出
    TempDataArray = tmp[y1:y2, x1:x2]
    #print(TempDataArray)

    # しきい値以上の温度データが得られたら、温度データを返却する
    if np.count_nonzero(TempDataArray >= TEMPERATURE_TH) >= AVERAGE_COUNT_TH:
        # 平均値出力
        if MEASUREMENT_METHOD == 0:
            #outTemp = np.average(TempDataArray)
            outTemp = TempDataArray[TempDataArray >= TEMPERATURE_TH].mean()
        # 最大値出力
        else:
            #outTemp = np.max(TempDataArray)
            outTemp = TempDataArray[TempDataArray >= TEMPERATURE_TH].max()

    #print("outTemp=%f" % outTemp)
    return outTemp
