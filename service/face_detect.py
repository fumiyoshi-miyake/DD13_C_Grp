# setting_facedetect.py

import tkinter as tk

from service.common import button_on, button_off, make_bg_canvas
from service.common import BG_ROW_WIDTH, BG_ROW1_HEIGHT, BG_ROW2_HEIGHT

from functools import partial

# 顔検出 [On: True, Off: False]
_is_facedetect_on = True


# ボタンフォントサイズ
FONT_SIZE_BTN = 14


# ------------------------------
# 戻るボタン押下時
# ------------------------------
def close_win(dlg):
    dlg.destroy()
    return


# ------------------------------
# 顔検出 On
# ------------------------------
def push_on():
    global _is_facedetect_on
    _is_facedetect_on = True

    button_on(button_facedetect_on, line_facedetect_on)
    button_off(button_facedetect_off, line_facedetect_off)

    return


# ------------------------------
# 顔検出 Off
# ------------------------------
def push_off():
    global _is_facedetect_on
    _is_facedetect_on = False

    button_off(button_facedetect_on, line_facedetect_on)
    button_on(button_facedetect_off, line_facedetect_off)
    
    return


# ------------------------------
# 顔検出 設定画面作成
# ------------------------------
def open_win():
    dlg = tk.Toplevel()
    #dlg.title('顔検出設定')
    #dlg.geometry('640x480')
    dlg.attributes('-fullscreen', True)
    dlg.grab_set()  # モーダル

    # Widget 作成
    #label_msg = tk.Label(dlg, text='顔検出', foreground='#0000FF', background='#FFFF00', font=("", 16))
    #label_msg = tk.Label(dlg, text='顔検出', foreground='#FFFFFF', background='#4472C4', font=("", 16))
    label_msg = tk.Label(dlg, text='顔検出', font=("", 16))
    label_msg.place(x=280, y=30)

    
    global button_facedetect_on
    global button_facedetect_off
    global line_facedetect_on
    global line_facedetect_off

    bg_width  = BG_ROW_WIDTH
    bg_height = BG_ROW1_HEIGHT
    line_facedetect_on  = make_bg_canvas(dlg, BG_ROW_WIDTH, BG_ROW1_HEIGHT)
    line_facedetect_off = make_bg_canvas(dlg, BG_ROW_WIDTH, BG_ROW1_HEIGHT)
    
    button_facedetect_on  = tk.Button(dlg, text='ON', width=11, height=3, \
                                font=('', FONT_SIZE_BTN), command=push_on) 
    button_facedetect_off = tk.Button(dlg, text='OFF', width=11, height=3, \
                                font=('', FONT_SIZE_BTN), command=push_off)
    button_back           = tk.Button(dlg, text='戻る', width=8, height=3, \
                                font=('', FONT_SIZE_BTN), command=partial(close_win, dlg)) 

    col = [150, 330]  # ボタンx座標
    row = 100  #ボタンy座標
    button_facedetect_on.place(x=col[0], y=row)
    button_facedetect_off.place(x=col[1], y=row)
    line_facedetect_on.place(x=col[0]-5, y=row-5)
    line_facedetect_off.place(x=col[1]-5, y=row-5)

    button_back.place(x=400, y=300)

    if _is_facedetect_on :
        push_on()
    else:
        push_off()

    return


# ------------------------------
# 
# ------------------------------
def set_facedetect(onoff):
    global _is_facedetect_on
    if onoff == 1:
        _is_facedetect_on = True
    else:
        _is_facedetect_on = False
    return

