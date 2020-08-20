# thermo_color : サーモグラフィ画像作成

from PIL import Image
import numpy as np
import cv2


# ------------------------------
# 温度 → BGR変換
# Input  : min  = 最小温度（Blue）
#          max  = 最大温度（Red）
#          temp = 入力温度
# Return : 入力温度のBGR値
# ------------------------------
def temp_to_bgr(min, max, temp):

  # 色閾値
  mid_cyan = (min*3 + max)/4
  mid_green = (min + max)/2
  mid_yellow = (min + max*3)/4

  # 温度 → BGR変換
  if temp <= min:    # Blue
    bgr = [255,0,0]
  elif temp < mid_cyan:
    mid = 255 * (temp - min) / (mid_cyan - min)
    bgr = [255, int(mid), 0]
  elif temp < mid_green:
    mid = 255 * (1 - (temp - mid_cyan) / (mid_green - mid_cyan) )
    bgr = [int(mid), 255, 0]
  elif temp < mid_yellow:
    mid = 255 * (temp - mid_green) / (mid_yellow - mid_green)
    bgr = [0, 255, int(mid)]
  elif temp < max:
    mid = 255 * (1 - (temp - mid_yellow) / (max - mid_yellow) )
    bgr = [0, int(mid), 255]
  elif temp >= max:  # Red
    bgr = [0,0,255]
  else:  # White
    bgr = [255,255,255]
    
  return bgr


# ------------------------------
# カラーバー作成
# Input  : min = 最小温度（Blue）
#          max = 最大温度（Red）
#          width  = 出力画像 水平画素数
#          height = 出力画像 垂直画素数
# Return : colorbar_array = カラーバー画像データ
# ------------------------------
def make_colorbar(min, max, width, height):
  min *= 10
  max *= 10
  temp_array = [[[0]*3 for x in range(width)] for i in range(max-min)]

  # 指定範囲(min〜max)のカラーバーを作成
  for temp in range(min, max, 1):
    color = temp_to_bgr(min, max, temp)
    for x in range(width):
      temp_array[max-temp-1][x] = color

  img = np.asarray(Image.fromarray(np.uint8(temp_array)))
  colorbar_array = cv2.resize(img, (width, height), interpolation = cv2.INTER_LINEAR)

  return colorbar_array

# ------------------------------
# 8x8データ → BGRデータ
# Input  : input_data = サーモセンサデータ（8×8二次元配列）
#          min, max   = カラーグラデーション最小最大値
# Output : bgr_array  = BGRデータ（RGB値の8×8二次元配列）
# Return : None
# ------------------------------
def thermo2bgr(input_data, min, max, bgr_array):
  for y in range(8):  # height,
    for x in range(8):  # width
      bgr_array[y][x] = temp_to_bgr(min, max, input_data[y][x])
  return


# ------------------------------
# 8x8データ → サーモグラフィ画像出力
# Input  : input_data = サーモセンサデータ（8×8二次元配列）
#          min, max   = カラーグラデーション最小最大値
#          width      = 出力画像水平サイズ
#          height     = 出力画像垂直サイズ
# Return : thermo_array = サーモグラフィ画像データ
# ------------------------------
def make_thermograph(input_data, min, max, width, height):
  bgr_array = [[[0]*3 for x in range(8)] for i in range(8)]  # 3次元RGBデータ（RGB値の二次元配列）

  # 入力データ→BGR配列データ
  thermo2bgr(input_data, min, max, bgr_array)

  # 配列データ→画像ファイル
  img = np.asarray(Image.fromarray(np.uint8(bgr_array)))
  thermo_array = cv2.resize(img, (width, height), interpolation = cv2.INTER_LINEAR)
  
  return thermo_array

