# pygame_util : 

import cv2  # 暫定変換処理でのみ使用
import subprocess
import pygame
from pygame.locals import *

import setting

import numpy as np
from thermo_color_pygame import temp_to_rgb
from thermo_color_pygame import thermo2rgb


# 入力ファイルパスが表示できなかった場合に表示する画像
READ_ERR_IMAGE = 'read_err_image.jpg'

# 表示ウィンドウ名
WIN_NAME = 'C_Grp'  # (仮)

# センサー座標
START_POS = (200, 80)
END_POS = (440, 420)
#SENSOR_RECT = (START_POS[0], START_POS[1], END_POS[0], END_POS[1])
SENSOR_RECT = (START_POS, (END_POS[0]-START_POS[0], END_POS[1]-START_POS[1]))

# ステータステキスト背景座標
#STATUS_START_POS = (72, 39)
#STATUS_END_POS   = (564, 79)
STATUS_START_POS = (72, START_POS[1]-42)
#STATUS_END_POS   = (564, START_POS[1]-2)
STATUS_RECT = (STATUS_START_POS, (492, 40))

# 温度テキスト背景座標
# TEMP_START_POS = (480, 360)
# TEMP_END_POS   = (550, 396)
TEMP_START_POS = (END_POS[0]+2, END_POS[1]-36)
#TEMP_END_POS   = (TEMP_START_POS[0]+70+6, END_POS[1])
TEMP_RECT = (TEMP_START_POS, (76, 36))

# 表示画面
_screen_pygame = None


# status文字列表示部
_status_text = None  # ステータス
_status_font = None

_text_bg_color = None # 背景色(status＆体温 共通)

# センサ範囲
_sensor_rect = None
    
# 体温表示部
_body_temp_rect = None  # 体温背景 矩形範囲
_body_temp_text = None  # 体温値テキスト
_body_temp_font = None

# フォント
if setting.mode == 0:
    #font_path = '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'
    #font_path = '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'
    FONT_JP = None  # ★仮★
else:
    # ubuntu
    #font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    FONT_JP = 'notoserifcjkjp'  # 日本語対応
    FONT_JP_B = 'notosanscjkjp'   # 日本語対応, bold?

# 終了ボタン
_end_button = None
_end_button_text = None
END_BUTTON_RECT = (0, 0, 40, 30)

# 文字色
COLOR_TEXT = (0, 0, 0)

# センサー枠 線色
COLOR_SENSOR = (0, 0, 0)

# ボタン色
COLOR_BUTTON = (196, 196, 196)
COLOR_BUTTON_FONT = (0, 0, 0)

# ------------------------------
# xrandr | grep '*'コマンドの実行
# ------------------------------
def command2pipe(cmd1, cmd2):
    p = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
    p.stdout.close()
    first_line, rest_lines = p2.communicate()
    return(first_line, rest_lines)

# ------------------------------
# 解像度の取得取得
# ------------------------------
def getResolution():
    cmd1 = ['xrandr']
    cmd2 = ['grep', '*']
    resolution_string, junk = command2pipe(cmd1, cmd2)
    resolution = resolution_string.split()[0]
    resolution = resolution.decode()
    width, height = resolution.split('x')
    mesg = "Resolution: %sx%s" % (width, height)
    print(mesg)
    return(width, height)


# ------------------------------
# カラーバー作成
# Input  : min = 最小温度（Blue）
#          max = 最大温度（Red）
#          width  = 出力画像 水平画素数
#          height = 出力画像 垂直画素数
# Return : colorbar_array = カラーバー画像データ
# ------------------------------
def make_colorbar(min, max, width, height):
    min = int(min*10)
    max = int(max*10)

    # 指定範囲(min〜max)のカラーバーを作成
    temp_array = [[[0]*3 for i in range(max-min)] for x in range(width)]
    for temp in range(min, max, 1):
        color = temp_to_rgb(min, max, temp)
        for x in range(width):
            temp_array[x][max-temp-1] = color

    # 配列データ → 画像ファイル
    img = np.asarray(temp_array)
    pygame_img = pygame.surfarray.make_surface(img)
    colorbar_img = pygame.transform.scale(pygame_img, (width, height))

    return colorbar_img


# ------------------------------
# センサーデータ → サーモグラフィ画像出力
# Input  : input_data = サーモセンサデータ（二次元配列）
#          sensor_width, sensor_height = サーモセンサデータサイズ
#          min, max   = カラーグラデーション最小最大値
#          width      = 出力画像水平サイズ
#          height     = 出力画像垂直サイズ
# Return : thermo_array = サーモグラフィ画像データ
# ------------------------------
def make_thermograph(input_data, sensor_width, sensor_height, min, max, width, height):
    # 3次元RGBデータ（RGB値の二次元配列）
    rgb_array = [[[0]*3 for i in range(sensor_height)] for x in range(sensor_width)]

    # 入力データ → RGB配列データ
    thermo2rgb(input_data, sensor_width, sensor_height, min, max, rgb_array)

    # 配列データ → 画像ファイル
    img = np.asarray(rgb_array)
    pygame_img = pygame.surfarray.make_surface(img)
  
    #thermo_array = pygame.transform.scale(pygame_img, (width, height))
    thermo_array = pygame.transform.smoothscale(pygame_img, (width, height))
      
    return thermo_array


# ------------------------------
# テキスト＆背景描画
# Input : text       = 表示文字列
#       : text_pos   = 表示座標
#       : rect       = 背景範囲
#       : rect_color = 背景色RGB
# ------------------------------
def draw_text_rect(text, text_pos, rect, rect_color):
    pygame.draw.rect(_screen_pygame, rect_color, rect)  # 指定色で塗り潰し
    _screen_pygame.blit(text, text_pos)

    return


# ------------------------------
# 表示ウィンドウ作成
# ------------------------------
def open_disp():
    #解像度取得
    #width_pixel, height_pixel = getResolution()
    width_pixel, height_pixel = ('640', '480')  # ★仮★

    pygame.init()
    global _screen_pygame
    _screen_pygame = pygame.display.set_mode((int(width_pixel), int(height_pixel)))
    pygame.display.set_caption(WIN_NAME) 

    # status文字列 背景範囲＆フォント作成
    global _status_text
    global _status_font
    #_status_font = pygame.font.SysFont(FONT_JP_B, 30)
    _status_font = pygame.font.SysFont(FONT_JP, 30)


    # センサー範囲
    global _sensor_rect
    _sensor_rect = pygame.Rect(SENSOR_RECT)
    
    # 体温表示部 背景範囲＆フォント作成
    global _body_temp_rect
    global _body_temp_text
    global _body_temp_font
    _body_temp_rect = pygame.Rect(TEMP_RECT)
    _body_temp_font = pygame.font.SysFont(None, 50)
    #_body_temp_font = pygame.font.SysFont(FONT_JP_B, 30)

    # ボタン作成
    global _end_button
    global _end_button_text
    _end_button = pygame.Rect(END_BUTTON_RECT)
    button_font = pygame.font.SysFont(FONT_JP, 14)
    _end_button_text = button_font.render('終了', True, COLOR_BUTTON_FONT)

    return
    

# ------------------------------
# 表示ウィンドウを閉じる
# ------------------------------
def close_disp():
    pygame.quit()
    exit()


# ------------------------------
# 画面に入力画像を出力する
# Input : img = 入力画像(pygame_img)
#       : body_temp = 体温
# ------------------------------
def out_disp(img, colorbar_img, status_text, status_pos, bg_color, body_temp, sensor_data):
    if img is None:
        # 指定パスの画像がない場合は既定ファイルを読み込む
        img = pygame.image.load(READ_ERR_IMAGE)
        if img is None:
            # 既定ファイルも開けなかった場合の処理（暫定）
            # 終了
            pygame.quit()
        return False

    # サーモグラフィ画像作成,
    if setting.sensor == 0:
        thermo_img = make_thermograph(sensor_data, 8, 8, setting.colorbar_min, setting.colorbar_max,\
                                      setting.thermo_width, setting.thermo_height)
    else:
        # 新センサ 80x60
        thermo_img = make_thermograph(sensor_data, 80, 60, setting.colorbar_min, setting.colorbar_max,\
                                      setting.thermo_width, setting.thermo_height)

    # 画像表示
    _screen_pygame.blit(img, (0, 0))
    _screen_pygame.blit(colorbar_img, (setting.comp_ofst_x, setting.comp_ofst_y))
    _screen_pygame.blit(thermo_img, (setting.comp_ofst_x+20, setting.comp_ofst_y))

    # センサ範囲矩形描画
    pygame.draw.rect(_screen_pygame, COLOR_SENSOR, SENSOR_RECT, 2)  # 枠線


    # ステータス表示
    _status_text = _status_font.render(status_text, True, COLOR_TEXT)
    draw_text_rect(_status_text, status_pos, STATUS_RECT, bg_color)

    # 体温表示
    if body_temp != 0:
        _body_temp_text = _body_temp_font.render(str(body_temp), True, COLOR_TEXT)
        draw_text_rect(_body_temp_text, (TEMP_START_POS[0]+5,TEMP_START_POS[1]+2), _body_temp_rect, bg_color)

    # ボタン追加 ★仮★
    draw_text_rect(_end_button_text, (5, 4), _end_button, COLOR_BUTTON)
    #pygame.draw.rect(_screen_pygame, (0, 0, 0), _end_button, width = 1)  # 黒色枠線

    # 表示更新
    pygame.display.update()

    # イベント取得
    for event in pygame.event.get():
        # 閉じるボタンが押された時の処理
        if event.type == QUIT:
            pygame.quit()
            return False

        # マウスイベント
        if event.type == pygame.MOUSEBUTTONDOWN:
            if _end_button.collidepoint(event.pos):
                pygame.quit()
                return False

    return True


# 暫定版 変換処理 (入力がPygameデータになれば変換は不要になるので削除する)
# see https://qiita.com/sounisi5011/items/f26e2756da774c164a47
def convert_opencv_img_to_pygame(opencv_image):
    """
    OpenCVの画像をPygame用に変換.

    see https://gist.github.com/radames/1e7c794842755683162b
    see https://github.com/atinfinity/lab/wiki/%5BOpenCV-Python%5D%E7%94%BB%E5%83%8F%E3%81%AE%E5%B9%85%E3%80%81%E9%AB%98%E3%81%95%E3%80%81%E3%83%81%E3%83%A3%E3%83%B3%E3%83%8D%E3%83%AB%E6%95%B0%E3%80%81depth%E5%8F%96%E5%BE%97
    """
    cvt_code = cv2.COLOR_BGR2RGB
    rgb_image = cv2.cvtColor(opencv_image, cvt_code).swapaxes(0, 1)
    # OpenCVの画像を元に、Pygameで画像を描画するためのSurfaceを生成する
    pygame_image = pygame.surfarray.make_surface(rgb_image)

    return pygame_image


