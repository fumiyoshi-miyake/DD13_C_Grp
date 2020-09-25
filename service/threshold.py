# threshold.py

import tkinter as tk
from tkinter import ttk
from functools import partial
import numpy as np

# 体温閾値
_temp_threshold_index = 5  #37.5
_temp_threshold = 37.5

# 体温閾値コンボボックスの上下限値
THRESHOLD_UPPER = 38.0
THRESHOLD_LOWER = 37.0

# 体温閾値コンボボックスの刻み
THRESHOLD_STEP = 0.1

# ボタンフォントサイズ
FONT_SIZE_BTN = 14


# ------------------------------
# 戻るボタン押下時
# ------------------------------
def close_win(dlg):
    global _temp_threshold_index
    global _temp_threshold
    global combo_threshold
    _temp_threshold_index = combo_threshold.current()
    _temp_threshold = combo_threshold.get()
    dlg.destroy()

    return


# ------------------------------
# 体温閾値 設定画面作成
# ------------------------------
def open_win():
    dlg = tk.Toplevel()
    #dlg.title('体温閾値設定')
    #dlg.geometry('640x480')
    dlg.attributes('-fullscreen', True)
    dlg.grab_set()  # モーダル

    # Widget 作成
    label_msg = tk.Label(dlg, text='体温閾値設定', font=('', 16))
    label_msg.place(x=250, y=30)

    # 文字間の空白部分にコンボボックスを重ねる
    label_threshold = tk.Label(dlg, text='異常とする体温　　　　　度以上', font=('', 16))
    label_threshold.place(x=125, y=100)

    global _temp_threshold_index
    global combo_threshold
    list_threshold = ['38.0', '37.9', '37.8', '37.7', '37.6', '37.5', '37.4', '37.3', '37.2', '37.1', '37.0']
    combo_threshold = ttk.Combobox(dlg, justify=tk.CENTER, \
                                values=list_threshold, \
                                width=6, state='readonly', font=('', 14))
    combo_threshold.grid(column=0, row=1)
    combo_threshold.current(_temp_threshold_index)

    button_back = tk.Button(dlg, text='戻る', width=8, height=3, \
                        font=('', FONT_SIZE_BTN), command=partial(close_win, dlg)) 

    # 配置
    combo_threshold.place(x=285, y=105)
    button_back.place(x=400, y=300)


    return

 
# ------------------------------
# ------------------------------
def set_threshold(threshold):
    global _temp_threshold_index
    global _temp_threshold

    # 温度からコンボボックスのインデックスを探索
    # 一致がなければデフォルト値
    index = 0
    for temp in range(int(THRESHOLD_UPPER*10), int(THRESHOLD_LOWER*10)-1, -int(THRESHOLD_STEP*10)):
        if temp == int(threshold*10):
           _temp_threshold_index = index
           _temp_threshold = threshold
           break
        index += 1 

    return

