# 温度測定判定で使用する温度しきい値
TEMPERATURE_TH = 35.5
# 温度測定判定で使用する温度しきい値以上のデータ数のしきい値
AVERAGE_COUNT_TH = 9
# 測定手法（0:平均値, 1:最大値）
MEASUREMENT_METHOD = 0

# 体温のオフセット値
OFFSET_TEMP = 6.0

# ------------------------------
# 温度データ取得
# ------------------------------
def getTempData(inTemp, isDetFace):
    outTemp = 0
    sumTemp = 0
    countTemp = 0
    maxTemp = 0

    # センサ解像度分ループ
    for i in range(8):
        for j in range(8):
            #オフセットは全データに加算
            inTemp[i][j] += OFFSET_TEMP
            
            # センサの有効範囲チェック 中央4x4を有効とする
            if i > 1 and i < 6 and j > 1 and j < 6:
                if TEMPERATURE_TH <= inTemp[i][j]:
                    countTemp += 1
                    sumTemp += inTemp[i][j]
                    if maxTemp < inTemp[i][j]:
                        maxTemp = inTemp[i][j]

    # 人物検出していない場合は0（無効値）を返す
    if isDetFace == False:
       return 0

    # しきい値以上の温度データが得られたら、温度データを返却する
    if countTemp >= AVERAGE_COUNT_TH:
       # 平均値出力
       if MEASUREMENT_METHOD == 0:
          outTemp = sumTemp / countTemp

       # 最大値出力
       else:
          outTemp = maxTemp
         
    return outTemp

