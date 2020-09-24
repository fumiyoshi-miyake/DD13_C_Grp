# thermo.py

import tkinter as tk

from functools import partial

import service.thermo_size as set_size
import service.thermo_pos as set_pos
import service.thermo_temp as set_temp

# ボタンフォントサイズ
FONT_SIZE_BTN = 14

# ------------------------------
# 戻るボタン押下時
# ------------------------------
def close_win(dlg):
    dlg.destroy()
    return


# ------------------------------
# サイズ設定
# ------------------------------
def push_set_size():
    set_size.open_win()
    return


# ------------------------------
# 位置設定
# ------------------------------
def push_set_pos():
    set_pos.open_win()
    return


# ------------------------------
# 温度設定
# ------------------------------
def push_set_temp():
    set_temp.open_win()
    return


# ------------------------------
# サーモグラフィ 設定画面作成
# ------------------------------
def open_win():
    dlg = tk.Toplevel()
    #dlg.title('サーモグラフィ設定')
    #dlg.geometry('640x480')
    dlg.attributes('-fullscreen', True)
    dlg.grab_set()  # モーダル

    # Widget 作成
    label_msg = tk.Label(dlg, text='サーモグラフィ', font=("", 16))
    label_msg.place(x=245, y=30)

    button_size = tk.Button(dlg, text='サイズ設定', width=11, height=3, \
                        font=('', FONT_SIZE_BTN), command=push_set_size) 
    button_pos  = tk.Button(dlg, text='位置設定', width=11, height=3, \
                        font=('', FONT_SIZE_BTN), command=push_set_pos)
    button_temp = tk.Button(dlg, text='温度設定', width=11, height=3, \
                        font=('', FONT_SIZE_BTN), command=push_set_temp)

    button_back = tk.Button(dlg, text='戻る', width=8, height=3, \
                        font=('', FONT_SIZE_BTN), command=partial(close_win, dlg)) 

    # 配置
    button_size.place(x=70, y=100)
    button_pos.place(x=240, y=100)
    button_temp.place(x=410, y=100)
    
    button_back.place(x=440, y=300)

    return


