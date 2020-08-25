# text_jp : 

from PIL import Image, ImageFont, ImageDraw
import numpy as np



# 画像に日本語文字を入れる関数
def putJapaneseText(img, message, pos, bgra):
    #font_path = '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'  # Windowsのフォントファイルへのパス
    font_path = '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'  # Windowsのフォントファイルへのパス
    font_size = 30                                      # フォントサイズ
    font = ImageFont.truetype(font_path, font_size)     # PILでフォントを定義
    img = Image.fromarray(img)                          # cv2(NumPy)型の画像をPIL型に変換
    draw = ImageDraw.Draw(img)                          # 描画用のDraw関数を用意

    # テキストを描画（位置、文章、フォント、文字色（BGR+α）を指定）
    draw.text(pos, message, font=font, fill=bgra)
    img = np.array(img)                                 # PIL型の画像をcv2(NumPy)型に変換
    return img                                          # 文字入りの画像をリターン

