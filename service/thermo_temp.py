# thermo_temp.py

import tkinter as tk
from tkinter import ttk
from functools import partial

import numpy as np

# 最高/最低温度
_temp_max_index = 2  # 40
_temp_min_index = 2  # 30
_temp_max = 40
_temp_min = 30

# 最高温度コンボボックスの上下限値
TEMP_MAX_UPPER = 50
TEMP_MAX_LOWER = 35
# 最低温度コンボボックスの上下限値
TEMP_MIN_UPPER = 30
TEMP_MIN_LOWER = 15

# 温度コンボボックスの刻み
TEMP_STEP = 5

# ボタンフォントサイズ
FONT_SIZE_BTN = 14


# ------------------------------
# 戻るボタン押下時
# ------------------------------
def close_win(dlg):
    global _temp_max_index
    global _temp_min_index
    global _temp_max
    global _temp_min
    global combo_temp_max
    global combo_temp_min
    _temp_max_index = combo_temp_max.current()
    _temp_min_index = combo_temp_min.current()
    _temp_max = combo_temp_max.get()
    _temp_min = combo_temp_min.get()

    dlg.destroy()

    return
    

# ------------------------------
# 温度範囲 設定画面作成
# ------------------------------
def open_win():
    dlg = tk.Toplevel()
    #dlg.title('サーモグラフィ温度範囲設定')
    #dlg.geometry('640x480')
    dlg.attributes('-fullscreen', True)
    dlg.grab_set()  # モーダル

    # Widget 作成
    label_msg = tk.Label(dlg, text='サーモグラフィ温度設定', font=('', 16))
    label_msg.place(x=190, y=30)

    label_temp_max = tk.Label(dlg, text='最高温度[℃]', font=('', 16))
    label_temp_max.place(x=150, y=100)
    label_temp_min = tk.Label(dlg, text='最低温度[℃]', font=('', 16))
    label_temp_min.place(x=150, y=160)

    global _temp_max_index
    global _temp_min_index
    global combo_temp_max
    global combo_temp_min
    combo_temp_max = ttk.Combobox(dlg, justify=tk.CENTER, \
                            values=list(range(TEMP_MAX_UPPER, TEMP_MAX_LOWER-1, -TEMP_STEP)), \
                            width=6, state='readonly', font=('', 14))
    combo_temp_max.grid(column=0, row=1)
    combo_temp_max.current(_temp_max_index)

    combo_temp_min = ttk.Combobox(dlg, justify=tk.CENTER, \
                            values=list(range(TEMP_MIN_UPPER, TEMP_MIN_LOWER-1, -TEMP_STEP)), \
                            width=6, state='readonly', font=('', 14))
    combo_temp_min.grid(column=0, row=1)
    combo_temp_min.current(_temp_min_index)

    button_back = tk.Button(dlg, text='戻る', width=8, height=3, \
                        font=('', FONT_SIZE_BTN), command=partial(close_win, dlg)) 

    # 配置
    combo_temp_max.place(x=290, y=106)
    combo_temp_min.place(x=290, y=166)
    button_back.place(x=400, y=300)


    return


# ------------------------------
# ------------------------------
def set_temp(max_temp, min_temp):
    global _temp_max_index
    global _temp_min_index
    global _temp_max
    global _temp_min

    max_list = range(TEMP_MAX_UPPER, TEMP_MAX_LOWER-1, -TEMP_STEP)
    min_list = range(TEMP_MIN_UPPER, TEMP_MIN_LOWER-1, -TEMP_STEP)

    # 温度からコンボボックスのインデックスを探索
    # 一致がなければデフォルト値
    index = 0
    for temp in range(TEMP_MAX_UPPER, TEMP_MAX_LOWER-1, -TEMP_STEP):
        if temp == max_temp:
           _temp_max_index = index
           _temp_max = temp
           break
        index += 1 

    index = 0
    for temp in range(TEMP_MIN_UPPER, TEMP_MIN_LOWER-1, -TEMP_STEP):
        if temp == min_temp:
           _temp_min_index = index
           _temp_min = temp
           break
        index += 1 


    return


