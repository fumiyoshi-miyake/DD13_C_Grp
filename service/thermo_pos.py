# thermo_pos.py

import tkinter as tk
from functools import partial
from enum import Enum

from service.common import button_on, button_off, make_bg_canvas
from service.common import BG_ROW_WIDTH, BG_ROW1_HEIGHT, BG_ROW2_HEIGHT


# 位置
class Pos(Enum):
    TOP_L = 0     # 左上
    TOP_R = 1     # 右上
    BOTTOM_L = 2  # 左下
    BOTTOM_R = 3  # 右下

# サーモグラフィ位置
_thermo_pos = Pos.BOTTOM_L

# ボタンフォントサイズ
FONT_SIZE_BTN = 14


# ------------------------------
# 戻るボタン押下時
# ------------------------------
def close_win(dlg):
    dlg.destroy()

    return


# ------------------------------
# 左上 ボタン
# ------------------------------
def push_left_top_pos():
    global _thermo_pos
    _thermo_pos = Pos.TOP_L

    button_on(button_left_top, line_left_top)
    button_off(button_right_top, line_right_top)
    button_off(button_left_bottom, line_left_bottom)
    button_off(button_right_bottom, line_right_bottom)

    return


# ------------------------------
# 右上 ボタン
# ------------------------------
def push_right_top_pos():
    global _thermo_pos
    _thermo_pos = Pos.TOP_R

    button_off(button_left_top, line_left_top)
    button_on(button_right_top, line_right_top)
    button_off(button_left_bottom, line_left_bottom)
    button_off(button_right_bottom, line_right_bottom)

    return


# ------------------------------
# 左下 ボタン
# ------------------------------
def push_left_bottom_pos():
    global _thermo_pos
    _thermo_pos = Pos.BOTTOM_L

    button_off(button_left_top, line_left_top)
    button_off(button_right_top, line_right_top)
    button_on(button_left_bottom, line_left_bottom)
    button_off(button_right_bottom, line_right_bottom)

    return


# ------------------------------
# 右下 ボタン
# ------------------------------
def push_right_bottom_pos():
    global _thermo_pos
    _thermo_pos = Pos.BOTTOM_R

    button_off(button_left_top, line_left_top)
    button_off(button_right_top, line_right_top)
    button_off(button_left_bottom, line_left_bottom)
    button_on(button_right_bottom, line_right_bottom)

    return


# ------------------------------
# サーモグラフィ 位置画面作成
# ------------------------------
def open_win():
    dlg = tk.Toplevel()
    #dlg.title('サーモグラフィ位置設定')
    #dlg.geometry('640x480')
    dlg.attributes('-fullscreen', True)
    dlg.grab_set()  # モーダル

    # Widget 作成
    label_msg = tk.Label(dlg, text='サーモグラフィ位置設定', font=("", 16))
    label_msg.place(x=190, y=30)
    
    #global _thermo_pos
    global button_left_top
    global button_right_top
    global button_left_bottom
    global button_right_bottom
    global line_left_top
    global line_right_top
    global line_left_bottom
    global line_right_bottom
 
    bg_width  = BG_ROW_WIDTH
    bg_height = BG_ROW2_HEIGHT
    line_left_top  = make_bg_canvas(dlg, bg_width, bg_height)
    line_right_top = make_bg_canvas(dlg, bg_width, bg_height)
    line_left_bottom  = make_bg_canvas(dlg, bg_width, bg_height)
    line_right_bottom = make_bg_canvas(dlg, bg_width, bg_height)
     
    button_left_top  = tk.Button(dlg, text='左上', width=11, height=2, \
                        font=('', FONT_SIZE_BTN), command=push_left_top_pos) 
    button_right_top = tk.Button(dlg, text='右上', width=11, height=2, \
                        font=('', FONT_SIZE_BTN), command=push_right_top_pos)
    button_left_bottom  = tk.Button(dlg, text='左下', width=11, height=2, \
                        font=('', FONT_SIZE_BTN), command=push_left_bottom_pos)
    button_right_bottom  = tk.Button(dlg, text='右下', width=11, height=2, \
                        font=('', FONT_SIZE_BTN), command=push_right_bottom_pos)


    button_back = tk.Button(dlg, text='戻る', width=8, height=3, \
                        font=('', FONT_SIZE_BTN), command=partial(close_win, dlg)) 

    # 配置
    col = [150, 330]  # ボタンx座標
    row = [100, 200]  # ボタンy座標

    button_left_top.place(x=col[0], y=row[0])
    button_right_top.place(x=col[1], y=row[0])
    line_left_top.place(x=col[0]-5, y=row[0]-5)
    line_right_top.place(x=col[1]-5, y=row[0]-5)

    button_left_bottom.place(x=col[0], y=row[1])
    button_right_bottom.place(x=col[1], y=row[1])
    line_left_bottom.place(x=col[0]-5, y=row[1]-5)
    line_right_bottom.place(x=col[1]-5, y=row[1]-5)
    
    button_back.place(x=440,y=300)


    if _thermo_pos == Pos.TOP_L:
        push_left_top_pos()
    elif _thermo_pos == Pos.TOP_R:
        push_right_top_pos()
    elif _thermo_pos == Pos.BOTTOM_L:
        push_left_bottom_pos()
    else:
        push_right_bottom_pos()

    return


