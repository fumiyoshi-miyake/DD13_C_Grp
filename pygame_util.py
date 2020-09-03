# pygame_util : 

import cv2
import subprocess
import pygame
from pygame.locals import *


# 入力ファイルパスが表示できなかった場合に表示する画像
READ_ERR_IMAGE = 'read_err_image.jpg'

# 表示ウィンドウ名
WIN_NAME = 'C_Grp'  # (仮)


_screen_pygame = None

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
# 表示ウィンドウ作成
# ------------------------------
def open_disp():
    #解像度取得
    #width_pixel, height_pixel = getResolution()
    width_pixel, height_pixel = ('640', '480')

    pygame.init()
    global _screen_pygame
    _screen_pygame = pygame.display.set_mode((int(width_pixel), int(height_pixel)))
    pygame.display.set_caption(WIN_NAME) 
    return
    

# ------------------------------
# 表示ウィンドウを閉じる
# ------------------------------
def close_disp():
    #print('close_disp_pygame')
    pygame.quit()
    exit()


# ------------------------------
# 画面に入力画像を出力する
# Input : img = 入力画像(pygame_img)
# ------------------------------
def out_disp(img):
    if img is None:
        # 指定パスの画像がない場合は既定ファイルを読み込む
        img = pygame.image.load(READ_ERR_IMAGE)
        if img is None:
            # 既定ファイルも開けなかった場合の処理（暫定）
            # 終了
            pygame.quit()
        return False

    # 画像表示
    _screen_pygame.blit(img, (0,0))
    pygame.display.update()

    for event in pygame.event.get():
        # 閉じるボタンが押された時の処理
        if event.type == QUIT:
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


