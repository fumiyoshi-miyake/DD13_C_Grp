#デバッグ出力はPythonコマンド実行時にO（大文字のオー）オプション付加

import numpy as np
import cv2
import csv

import setting




if setting.mode == 1 :
  #シュミレート用のサーモセンサーデータ 
  sensor_file = "sensorData.csv"
  #シュミレート用サーモセンサデータの読み込み対象データ（10パターンを周期的に読み込む）
  snsor_data_count = 0
  #サーモセンサーデータ数
  sensorCount = 64 
  #サーモセンサーのデータ配列
  temperature = [0] * sensorCount

  #シュミレート用の画像データ 
  pic_list = ["picture0.jpg", "picture1.jpg", "picture2.jpg", "picture3.jpg", "picture4.jpg", "picture5.jpg", "picture6.jpg", "picture7.jpg", "picture8.jpg", "picture9.jpg"]

  #シュミレート用画像データの読み込み対象データ（10パターンを周期的に読み込む）
  pic_data_count = 0

#サーモセンサーのデータ読み込み
def readTemp():
    if setting.mode == 1:
        global snsor_data_count
        with open(sensor_file) as f:
            sensorData = [row for row in csv.reader(f)]
        
        #特定の列の64行分のデータを取得
        for row in range(64):
            temperature[row] = float(sensorData[row][snsor_data_count])

        #10個読み込んだ場合は先頭に戻す
        if snsor_data_count == 9:
            snsor_data_count = 0
        else:
            #次に読むターゲットデータを進める
            snsor_data_count += 1   
        return temperature
    else:
        pass

#画像データの読み込み
def readPic():
    if setting.mode == 1:
        global pic_data_count
        image = cv2.imread(pic_list[pic_data_count])
        #10個読み込んだ場合は先頭に戻す
        if pic_data_count == 9:
            pic_data_count = 0
        else:
            #次に読むターゲットデータを進める
            pic_data_count += 1   
        return image
    else:
        pass
