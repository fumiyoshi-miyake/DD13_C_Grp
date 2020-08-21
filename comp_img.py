# comp_img : 画像合成

# カラーバー画像とサーモグラフィ画像の間隔
thermo_interval = 10

# ------------------------------
# 画像合成
# Input  : cam_img_path    = カメラ画像
#          colbar_img_path = カラーバー画像
#          thermo_img_path = サーモグラフィ画像
#          x_ofst, y_ofst  = 合成位置
# Return : cam_img         = 合成結果画像
# ------------------------------
def comp_thermo(cam_img, colbar_img, thermo_img, x_ofst, y_ofst):
 
  # 合成画像サイズ取得
  barsize_width  = colbar_img.shape[1]
  barsize_height = colbar_img.shape[0]
  thermo_width   = thermo_img.shape[1]
  thermo_height  = thermo_img.shape[0]

  # カラーバー画像を合成
  cam_img[y_ofst:barsize_height + y_ofst, x_ofst:barsize_width + x_ofst] = colbar_img

  # サーモグラフィ画像を合成
  x_ofst = x_ofst + barsize_width + thermo_interval
  cam_img[y_ofst:thermo_height + y_ofst, x_ofst:thermo_width + x_ofst] = thermo_img

  return cam_img


