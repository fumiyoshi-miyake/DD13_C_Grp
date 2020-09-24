import numpy as np
import cv2
import csv
import setting

if setting.mode == 1 :
    #シュミレート用サーモセンサデータの読み込み対象データ（8パターンを周期的に読み込む）
    snsor_data_count = 0

    if setting.sensor == 0:
        #シュミレート用の8×8サーモセンサーデータ 
        sensor_file = "sensorData.csv"
        #8×8センサー
        temperature = [[0]*8]*8
        #1パターンあたりの行数,列数
        row_count=8
        col_count=8

    else:
        #シュミレート用の80×60サーモセンサーデータ 
        sensor_file = "sensorDataLepton.csv"
        #80×60センサー
        temperature = [[0]*80]*60
        #1パターンあたりの行数,列数
        row_count=60
        col_count=80

    #シュミレート用の画像データ 
    pic_list = ["picture0.jpg", "picture1.jpg", "picture2.jpg", "picture3.jpg", "picture4.jpg", "picture5.jpg", "picture6.jpg", "picture7.jpg", "picture8.jpg", "picture9.jpg", "picture10.jpg", "picture11.jpg", "picture12.jpg", "picture13.jpg", "picture14.jpg", "picture15.jpg", "picture16.jpg", "picture17.jpg", "picture18.jpg", "picture19.jpg"]

    #シュミレート用画像データの読み込み対象データ（8パターンを周期的に読み込む）
    pic_data_count = 0

    #サーモセンサーのデータ読み込み
    def readTemp():
        if setting.mode == 1:
            global snsor_data_count
            with open(sensor_file) as f:
                sensorData = [row for row in csv.reader(f)]

            #1パターンのデータを取得
            for row in range(row_count):
                l_sf = sensorData[snsor_data_count * row_count + row]
                l_sf_f = [float(s) for s in l_sf]
                temperature[row] = l_sf_f


            #20個読み込んだ場合は先頭に戻す
            if snsor_data_count == 19:
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
            #8個読み込んだ場合は先頭に戻す
            if pic_data_count == 19:
                pic_data_count = 0
            else:
                #次に読むターゲットデータを進める
                pic_data_count += 1   
            return image
        else:
            pass
else:
    if setting.sensor == 0:
        row_count=8
        col_count=8
    else:
        row_count=60
        col_count=80
