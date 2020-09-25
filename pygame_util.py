# pygame_util : 

import cv2  # 暫定変換処理でのみ使用
import subprocess
import pygame
from pygame.locals import *

import setting

import numpy as np
from thermo_color_pygame import temp_to_rgb
from thermo_color_pygame import thermo2rgb

from service.thermo_size import Size
from service.thermo_pos import Pos

import time

# 入力ファイルパスが表示できなかった場合に表示する画像
READ_ERR_IMAGE = 'read_err_image.jpg'

# 表示ウィンドウ名
WIN_NAME = 'C_Grp'  # (仮)

# センサー座標
if setting.sensor == 0:
    SENSOR_RECT_FACE_ON = ((0, 0), (640,480))
    if setting.measure_mode == 0:
        # 顔
        START_POS = (180, 80)
        END_POS = (460, 340)
    else:
        # 手首
        START_POS = (200, 80)
        END_POS = (440, 420)
else:
    START_POS = (220, 80)
    END_POS = (420, 280)
    SENSOR_RECT_FACE_ON = ((60, 70), (480,360))
    
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
    FONT_JP = 'notoserifcjkjp'  # 日本語対応
    FONT_JP_B = 'notosanscjkjp'   # 日本語対応, bold?
else:
    # ubuntu
    #font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    FONT_JP = 'notoserifcjkjp'  # 日本語対応
    FONT_JP_B = 'notosanscjkjp'   # 日本語対応, bold?


# 文字色
COLOR_TEXT = (0, 0, 0)

# センサー枠 線色
COLOR_SENSOR = (0, 0, 0)

# ボタン色
COLOR_BUTTON = (196, 196, 196)
COLOR_BUTTON_FONT = (0, 0, 0)

# 長押し判定用
_press_count = 0
_long_press = False

# サーモグラフィ画像サイズ
_thermo_grf_width  = setting.thermo_width
_thermo_grf_height = setting.thermo_height

# サービスモードで変更可能な設定値
_face_detect = setting.face_detect  # 顔検出On/Off設定
_thermo_size = Size.M  # サーモグラフィ画像サイズ設定
_thermo_pos = Pos.BOTTOM_L  # サーモグラフィ画像位置設定
_thermo_max = setting.colorbar_max  # サーモグラフィ最高温度設定
_thermo_min = setting.colorbar_min  # サーモグラフィ最低温度設定
_thermo_threshold = '37.5' # 体温閾値設定

# ------------------------------
# サービスモードで変更可能な設定値の設定
# face_detect : 顔検出On/Off設定
# size : サーモグラフィ画像サイズ設定
# pos  : サーモグラフィ画像位置設定
# temp_max, temp_min : サーモグラフィ最高/最低温度設定
# temp_threshold : 体温閾値設定
# ------------------------------
def set_param(face_detect, size, pos, temp_max, temp_min, temp_threshold):
    global _face_detect
    global _thermo_size
    global _thermo_pos
    global _thermo_max
    global _thermo_min
    global _thermo_threshold
    _face_detect = face_detect
    _thermo_size = size
    _thermo_pos = pos
    _thermo_max = temp_max
    _thermo_min = temp_min
    _thermo_threshold = temp_threshold
    return

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
# Input  : width  = 出力画像 水平画素数
#          height = 出力画像 垂直画素数
# Return : colorbar_array = カラーバー画像データ
# ------------------------------
def make_colorbar(width, height):
    temp_min = int(_thermo_min*10)
    temp_max = int(_thermo_max*10)

    # 指定範囲(min〜max)のカラーバーを作成
    temp_array = [[[0]*3 for i in range(temp_max-temp_min)] for x in range(width)]
    for temp in range(temp_min, temp_max, 1):
        color = temp_to_rgb(temp_min, temp_max, temp)
        for x in range(width):
            temp_array[x][temp_max-temp-1] = color

    # 配列データ → 画像ファイル
    img = np.asarray(temp_array)
    pygame_img = pygame.surfarray.make_surface(img)
    colorbar_img = pygame.transform.scale(pygame_img, (width, height))

    return colorbar_img


# ------------------------------
# センサーデータ → サーモグラフィ画像出力
# Input  : input_data = サーモセンサデータ（二次元配列）
#          sensor_width, sensor_height = サーモセンサデータサイズ
#          width      = 出力画像水平サイズ
#          height     = 出力画像垂直サイズ
# Return : thermo_array = サーモグラフィ画像データ
# ------------------------------
def make_thermograph(input_data, sensor_width, sensor_height, width, height):
    # 3次元RGBデータ（RGB値の二次元配列）
    rgb_array = [[[0]*3 for i in range(sensor_height)] for x in range(sensor_width)]

    # 入力データ → RGB配列データ
    thermo2rgb(input_data, sensor_width, sensor_height, _thermo_min, _thermo_max, rgb_array)

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

    # マウス非表示化
    pygame.mouse.set_visible(False)

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
# Return1 : True: 成功, False: エラー,
# Return2 : True: 長押し, 
# ------------------------------
def out_disp(img, colorbar_img, status_text, status_pos, bg_color, body_temp, sensor_data, face_rect):
    global _face_detect
    if img is None:
        # 指定パスの画像がない場合は既定ファイルを読み込む
        img = pygame.image.load(READ_ERR_IMAGE)
        if img is None:
            # 既定ファイルも開けなかった場合の処理（暫定）
            # 終了
            pygame.quit()
        return False, False

    # サーモグラフィ画像作成,
    global _thermo_grf_width, _thermo_grf_height
    if setting.sensor == 0:
        thermo_img = make_thermograph(sensor_data, 8, 8, _thermo_grf_width, _thermo_grf_height)
    else:
        # 時間計測開始
        #t1 = time.time()
        # 新センサ 80x60
        thermo_img = make_thermograph(sensor_data, 80, 60, _thermo_grf_width, _thermo_grf_height)
        #時間計測終了
        #t2 = time.time()
        #elapsed_time = t2 - t1
        #print(f"経過時間：{elapsed_time}")

    # 画像表示
    _screen_pygame.blit(img, (0, 0))
    if setting.colorbar_width > 0:
        _screen_pygame.blit(colorbar_img, (setting.comp_ofst_x, setting.comp_ofst_y))
    if setting.thermo_width > 0:
        _screen_pygame.blit(thermo_img, (setting.comp_ofst_x+20, setting.comp_ofst_y))

    # センサ範囲矩形描画
    if _face_detect == 0:
        pygame.draw.rect(_screen_pygame, COLOR_SENSOR, SENSOR_RECT, 2)  # 枠線
    else:
        if setting.sensor == 1: 
            pygame.draw.rect(_screen_pygame, COLOR_SENSOR, SENSOR_RECT_FACE_ON, 2)  # 枠線

    # 顔枠表示 顔検出時
    if face_rect[2] != 0:
        pygame.draw.rect(_screen_pygame, bg_color, face_rect, 2)  # 枠線

    # ステータス表示
    _status_text = _status_font.render(status_text, True, COLOR_TEXT)
    draw_text_rect(_status_text, status_pos, STATUS_RECT, bg_color)

    # 体温表示
    if body_temp != 0:
        _body_temp_text = _body_temp_font.render(str(body_temp), True, COLOR_TEXT)
        if _face_detect == 0:
            draw_text_rect(_body_temp_text, (TEMP_START_POS[0]+5,TEMP_START_POS[1]+2), _body_temp_rect, bg_color)
        else:
            # 右端チェック はみ出す場合は左側に表示 +100はテキストサイズ＋オフセット
            if face_rect[0]+face_rect[2] + 100 > 640:
                TempStartPos = (face_rect[0]-76, face_rect[1]+face_rect[3] - 40)
            else:
                TempStartPos = (face_rect[0]+face_rect[2], face_rect[1]+face_rect[3] - 40)

            # 温度背景テキスト位置セット
            TempRect = (TempStartPos, (76, 36))
            bodyTempRect = pygame.Rect(TempRect)
            draw_text_rect(_body_temp_text, TempStartPos, bodyTempRect, bg_color)

    # 表示更新
    pygame.display.update()


    global _press_count
    global _long_press
    # イベント取得
    for event in pygame.event.get():
        # 閉じるボタンが押された時の処理
        if event.type == QUIT:
            pygame.quit()
            return False, False

        # マウスイベント
        elif event.type == pygame.MOUSEBUTTONUP:
            # 長押しカウントクリア
            _press_count = 0
            if _long_press:
                # サービスモード起動
                _long_press = False
                return True, True

    # 長押し判定
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:
        _press_count += 1
        if _press_count > 10:   # 一定のカウント以上で長押しと判定
            print('長押し検出！')
            _long_press = True


    return True, False


# ------------------------------
# 起動中メッセージを表示
# Input : 
#       : 
# ------------------------------
def startMsg_disp():
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    start_msg = pygame.image.load("start_msg.jpg")
    screen.blit(start_msg, (0, 0))
    pygame.display.update()


# ------------------------------
# ------------------------------
def set_thermo_size(width, height):
    global _thermo_grf_width, _thermo_grf_height
    _thermo_grf_width  = width
    _thermo_grf_height = height
    return


# ------------------------------
# 起動中メッセージを表示
# Input : 
#       : 
# ------------------------------
def startMsg_disp():
    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    start_msg = pygame.image.load("start_msg.jpg")
    screen.blit(start_msg, (0, 0))
    pygame.display.update()


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


