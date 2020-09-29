# common.py

import tkinter as tk
import setting

# 色
COLOR_BG_DEF = '#D9D9D9'  # 背景 初期色

# フォントサイズ
FONT_SIZE_BTN = 14

# 強調表示（ボタン背景Canvas）設定
BUTTON_BG_COLOR = 'black'

# 選択状態矩形サイズ
# 実機
if setting.mode == 0:
    BG_ROW_WIDTH   = 134
    BG_ROW1_HEIGHT = 83   # 1行用
    BG_ROW2_HEIGHT = 62   # 2行用
else:
    BG_ROW_WIDTH   = 157
    BG_ROW1_HEIGHT = 106  # 1行用
    BG_ROW2_HEIGHT = 79   # 2行用

# ------------------------------
# ボタン 選択
# ------------------------------
def button_on(button, canvas):
    #button['font']  = ('', FONT_SIZE_BTN, 'bold', 'underline')
    #button['font']  = ('', FONT_SIZE_BTN, 'underline')
    button['font']  = ('', FONT_SIZE_BTN)

    canvas['bg'] = 'black'  # 背景黒色（縁取り風表示になる）
    
    return


# ------------------------------
# ボタン 非選択
# ------------------------------
def button_off(button, canvas):
    button['font'] = ('', FONT_SIZE_BTN)
    canvas['bg'] = COLOR_BG_DEF
    
    return


# ------------------------------
# 強調表示用 背景canvas作成
# ------------------------------
def make_bg_canvas(dlg, bg_width, bg_height):
    return tk.Canvas(dlg, width=bg_width, height=bg_height, bg=BUTTON_BG_COLOR)

