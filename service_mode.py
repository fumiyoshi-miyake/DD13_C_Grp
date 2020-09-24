# service_mode.py

import tkinter as tk
import os
import csv
from functools import partial

import service.face_detect as set_face
import service.thermo as set_thermo
import service.threshold as set_threshold

SERVICE_CSV_FILE = 'service.csv'

# ボタンフォントサイズ
FONT_SIZE_BTN = 14

# ------------------------------
# 顔検出ボタン押下時の処理
# ------------------------------
def push_facedetect():
    #print('push face detect button')
    set_face.open_win()
    return


# ------------------------------
# サーモグラフィボタン押下時の処理
# ------------------------------
def push_thermo():
    #print('push thermo button')
    set_thermo.open_win()
    return


# ------------------------------
# 閾値ボタン押下時の処理
# ------------------------------
def push_threshold():
    #print('push threshold button')
    set_threshold.open_win()
    return


# ------------------------------
# 戻るボタン押下時の処理
# ------------------------------
def push_back():
    #print('push back button')

    # サービスモード画面を閉じる
    global _service_win
    _service_win.destroy()

    # 設定ファイル出力
    '''
    print('顔検出: {}'.format(set_face._is_facedetect_on))
    print('サーモグラフィ_サイズ: {}'.format(set_thermo.set_size._thermo_size.name))
    print('サーモグラフィ_位置: {}'.format(set_thermo.set_pos._thermo_pos.name))
    print('サーモグラフィ_最高温度: {}'.format(set_thermo.set_temp._temp_max))
    print('サーモグラフィ_最低温度: {}'.format(set_thermo.set_temp._temp_min))
    print('体温閾値: {}'.format(set_threshold._temp_threshold))
    '''
    with open(SERVICE_CSV_FILE, 'w') as ofile:
        writer = csv.writer(ofile)
        writer.writerow(['face_det', set_face._is_facedetect_on])
        writer.writerow(['thermo_size', set_thermo.set_size._thermo_size.name])
        writer.writerow(['thermo_pos', set_thermo.set_pos._thermo_pos.name])
        writer.writerow(['thermo_max', set_thermo.set_temp._temp_max])
        writer.writerow(['thermo_min', set_thermo.set_temp._temp_min])
        writer.writerow(['threshold', set_threshold._temp_threshold])

    return


# ------------------------------
# CSVファイル読み込み
# Return : face_det, thermo_size, thermo_pos,
#        : thermo_max, thermo_min, threshold,
# ------------------------------
def read_service_csv():
    face_det = 1
    thermo_size = set_thermo.set_size.Size.M
    thermo_pos = set_thermo.set_pos.Pos.BOTTOM_L
    thermo_max = '40'
    thermo_min = '25'
    thermo_threshold = '37.5'

    with open(SERVICE_CSV_FILE, 'r') as ifile:
        reader = csv.reader(ifile)
        for row in reader:
            if row[0] == 'face_det':
                #print(' detect_1 = {}'.format(row[1]))
                if row[1] == 'True':
                    face_det = 1
                else:
                    face_det = 0
            elif row[0] == 'thermo_size':
                #print(' detect_2 = {}'.format(row[1]))
                thermo_size = row[1]
            elif row[0] == 'thermo_pos':
                #print(' detect_3 = {}'.format(row[1]))
                thermo_pos = row[1]
            elif row[0] == 'thermo_max':
                #print(' detect_4 = {}'.format(row[1]))
                thermo_max = row[1]
            elif row[0] == 'thermo_min':
                #print(' detect_5 = {}'.format(row[1]))
                thermo_min = row[1]
            elif row[0] == 'threshold':
                #print(' detect_6 = {}'.format(row[1]))
                thermo_threshold = row[1]
            else:
                print('else param = {}'.format(row[1]))

    return face_det, thermo_size, thermo_pos, thermo_max, thermo_min, thermo_threshold


# ------------------------------
# システム終了ボタン押下時の処理
# ------------------------------
def push_end():
    print('push shutdown button')
    # シャットダウン
    #os.system('sudo shutdown -h now')
    exit()  # ★仮★
    return


# ------------------------------
# サービスモード起動
# ------------------------------
def open_service_mode():
    global _service_win
    _service_win = tk.Tk()
    _service_win.title('サービスモード')
    #_service_win.geometry('640x480')
    _service_win.attributes('-fullscreen', True)
    #_service_win.grab_set()  # モーダル


    # ボタン作成
    # widthはテキスト単位 (not pix)
    BTN_W = 20  # button_width
    BTN_H = 3   # button_height
    button_facedetect = tk.Button(text='顔検出', width=BTN_W, height=BTN_H, \
                            font=('', FONT_SIZE_BTN), command=push_facedetect) 
    button_thermo = tk.Button(text='サーモグラフィ', width=BTN_W, height=BTN_H, \
                            font=('', FONT_SIZE_BTN), command=push_thermo)
                           
    button_threshold = tk.Button(text='体温閾値', width=BTN_W, height=BTN_H, \
                            font=('', FONT_SIZE_BTN), command=push_threshold)

    button_back = tk.Button(text='戻る', width=BTN_W, height=BTN_H, \
                            font=('', FONT_SIZE_BTN), command=push_back) 
    button_end  = tk.Button(text='システム終了', width=BTN_W, height=BTN_H, \
                            font=('', FONT_SIZE_BTN), command=push_end)

    # ボタン配置
    col = [50, 340]       # ボタンx座標
    row = [30, 150, 300]  # ボタンy座標
    button_facedetect.place(x=col[0], y=row[0])
    button_thermo.place(x=col[1], y=row[0])
    button_threshold.place(x=col[0], y=row[1])

    button_back.place(x=col[0], y=row[2])
    button_end.place(x=col[1], y=row[2])


    _service_win.mainloop()

    return


# test_main
#open_service_mode()

