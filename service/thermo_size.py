# thermo_size.py

import tkinter as tk
from functools import partial
from enum import Enum

from service.common import button_on, button_off, make_bg_canvas
from service.common import BG_ROW_WIDTH, BG_ROW1_HEIGHT, BG_ROW2_HEIGHT

# サイズ
class Size(Enum):
    L = 0     # 1.5倍
    M = 1     # 標準
    S = 2     # 0.8倍
    ALL = 3   # 全画面表示
    HIDE = 4  # 非表示

# サーモグラフィサイズ
_thermo_size = Size.M

# ボタンフォントサイズ
FONT_SIZE_BTN = 14


# ------------------------------
# 戻るボタン押下時
# ------------------------------
def close_win(dlg):
    dlg.destroy()

    return


# ------------------------------
# 大 ボタン
# ------------------------------
def push_large_size():
    global _thermo_size
    _thermo_size = Size.L

    button_on(button_large, line_large)
    button_off(button_middle, line_middle)
    button_off(button_small, line_small)
    button_off(button_all, line_all)
    button_off(button_hide, line_hide)

    return


# ------------------------------
# 中 ボタン
# ------------------------------
def push_middle_size():
    global _thermo_size
    _thermo_size = Size.M

    button_off(button_large, line_large)
    button_on(button_middle, line_middle)
    button_off(button_small, line_small)
    button_off(button_all, line_all)
    button_off(button_hide, line_hide)

    return


# ------------------------------
# 小 ボタン
# ------------------------------
def push_small_size():
    global _thermo_size
    _thermo_size = Size.S

    button_off(button_large, line_large)
    button_off(button_middle, line_middle)
    button_on(button_small, line_small)
    button_off(button_all, line_all)
    button_off(button_hide, line_hide)

    return


# ------------------------------
# 全画面表示 ボタン
# ------------------------------
def push_all_size():
    global _thermo_size
    _thermo_size = Size.ALL

    button_off(button_large, line_large)
    button_off(button_middle, line_middle)
    button_off(button_small, line_small)
    button_on(button_all, line_all)
    button_off(button_hide, line_hide)

    return


# ------------------------------
# 非表示 ボタン
# ------------------------------
def push_hide_size():
    global _thermo_size
    _thermo_size = Size.HIDE

    button_off(button_large, line_large)
    button_off(button_middle, line_middle)
    button_off(button_small, line_small)
    button_off(button_all, line_all)
    button_on(button_hide, line_hide)

    return

# ------------------------------
# サーモグラフィ サイズ設定画面作成
# ------------------------------
def open_win():
    dlg = tk.Toplevel()
    #dlg.title('サーモグラフィサイズ設定')
    #dlg.geometry('640x480')
    dlg.attributes('-fullscreen', True)
    dlg.grab_set()  # モーダル

    # Widget 作成
    label_msg = tk.Label(dlg, text='サーモグラフィサイズ設定', font=("", 16))
    label_msg.place(x=190, y=30)
    
    #global _thermo_size
    global button_large
    global button_middle
    global button_small
    global button_all
    global button_hide
    global line_large
    global line_middle
    global line_small
    global line_all
    global line_hide

    bg_width  = BG_ROW_WIDTH
    bg_height = BG_ROW2_HEIGHT
    line_large  = make_bg_canvas(dlg, bg_width, bg_height)
    line_middle = make_bg_canvas(dlg, bg_width, bg_height)
    line_small  = make_bg_canvas(dlg, bg_width, bg_height)
    line_all  = make_bg_canvas(dlg, bg_width, bg_height)
    line_hide = make_bg_canvas(dlg, bg_width, bg_height)
    
    button_large  = tk.Button(dlg, text='大', width=11, height=2, \
                        font=('', FONT_SIZE_BTN), command=push_large_size) 
    button_middle = tk.Button(dlg, text='中', width=11, height=2, \
                        font=('', FONT_SIZE_BTN), command=push_middle_size)
    button_small  = tk.Button(dlg, text='小', width=11, height=2, \
                        font=('', FONT_SIZE_BTN), command=push_small_size)

    button_all  = tk.Button(dlg, text='全画面表示', width=11, height=2, \
                        font=('', FONT_SIZE_BTN), command=push_all_size)
    button_hide = tk.Button(dlg, text='非表示', width=11, height=2, \
                        font=('', FONT_SIZE_BTN), command=push_hide_size)

    button_back = tk.Button(dlg, text='戻る', width=8, height=3, \
                        font=('', FONT_SIZE_BTN), command=partial(close_win, dlg)) 

    # 配置
    col = [70, 240, 410]  # ボタンx座標
    row = [100, 200]      # ボタンy座標
    button_large.place(x=col[0], y=row[0])
    button_middle.place(x=col[1], y=row[0])
    button_small.place(x=col[2], y=row[0])
    line_large.place(x=col[0]-5, y=row[0]-5)
    line_middle.place(x=col[1]-5, y=row[0]-5)
    line_small.place(x=col[2]-5, y=row[0]-5)

    button_all.place(x=col[0], y=row[1])
    button_hide.place(x=col[1], y=row[1])
    line_all.place(x=col[0]-5, y=row[1]-5)
    line_hide.place(x=col[1]-5, y=row[1]-5)
    
    button_back.place(x=400, y=300)


    if _thermo_size == Size.L:
        push_large_size()
    elif _thermo_size == Size.M:
        push_middle_size()
    elif _thermo_size == Size.S:
        push_small_size()
    elif _thermo_size == Size.ALL:
        push_all_size()
    else:
        push_hide_size()

    return



# ------------------------------
# 
# ------------------------------
def set_size(size):
    global _thermo_size

    if size == 'L':
        _thermo_size = Size.L
    elif size == 'M':
        _thermo_size = Size.M
    elif size == 'S':
        _thermo_size = Size.S
    elif size == 'ALL':
        _thermo_size = Size.ALL
    elif size == 'HIDE':
        _thermo_size = Size.HIDE
    else:
        _thermo_size = Size.M

    return

