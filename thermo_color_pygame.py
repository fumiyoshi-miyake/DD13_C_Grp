# thermo_color : サーモグラフィデータ作成


# ------------------------------
# 温度 → RGB変換
# Input  : min  = 最小温度（Blue）
#          max  = 最大温度（Red）
#          temp = 入力温度
# Return : 入力温度のRGB値
# ------------------------------
def temp_to_rgb(min, max, temp):

    # 色閾値
    mid_cyan = (min*3 + max)/4
    mid_green = (min + max)/2
    mid_yellow = (min + max*3)/4

    # 温度 → RGB変換
    if temp <= min:    # Blue
        rgb = [0, 0, 255]
 
    elif temp < mid_cyan:
        mid = 255 * (temp - min) / (mid_cyan - min)
        rgb = [0, int(mid), 255]
 
    elif temp < mid_green:
        mid = 255 * (1 - (temp - mid_cyan) / (mid_green - mid_cyan) )
        rgb = [0, 255, int(mid)]
 
    elif temp < mid_yellow:
        mid = 255 * (temp - mid_green) / (mid_yellow - mid_green)
        rgb = [int(mid), 255, 0]
 
    elif temp < max:
        mid = 255 * (1 - (temp - mid_yellow) / (max - mid_yellow) )
        rgb = [255, int(mid), 0]
 
    elif temp >= max:  # Red
        rgb = [255, 0, 0]
 
    else:  # White
        rgb = [255, 255, 255]
 
    return rgb
  
  
# ------------------------------
# センサーデータ → RGBデータ
# Input  : input_data = サーモセンサデータ（二次元配列）
#          sensor_width, sensor_height = サーモセンサデータサイズ
#          min, max   = カラーグラデーション最小最大値
# Output : rgb_array  = RGBデータ（RGB値の二次元配列）
# Return : None
# ------------------------------
def thermo2rgb(input_data, sensor_width, sensor_height, min, max, rgb_array):
  for y in range(sensor_height):
    for x in range(sensor_width):
      rgb_array[x][y] = temp_to_rgb(min, max, input_data[y][x])
  return



  
