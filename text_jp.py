# text_jp : 

from PIL import Image, ImageFont, ImageDraw
import numpy as np
import setting

# フォントファイルへのパス
if setting.mode == 0:
  #font_path = '/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf'
  font_path = '/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf'
else:
  # ubuntu
  font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

# フォントサイズ
font_size = 30

# ------------------------------
# 画像に日本語文字を入れる関数
# Input  : img     = 画像データ
#        : message = 入力文字列
#        : pos     = 文字位置
#        : bgra    = 文字色
# Return : out_img = 文字を追加した画像データ
# ------------------------------
def putJapaneseText(img, message, pos, bgra):
    # PILでフォントを定義
    font = ImageFont.truetype(font_path, font_size)

    # cv2(NumPy)型の画像をPIL型に変換
    pil_img = Image.fromarray(img)

    # 描画用のDraw関数を用意
    draw = ImageDraw.Draw(pil_img)

    # テキストを描画（位置、文章、フォント、文字色（BGR+α）を指定）
    draw.text(pos, message, font=font, fill=bgra)

    # PIL型の画像をcv2(NumPy)型に変換
    out_img = np.array(pil_img)

    return out_img


