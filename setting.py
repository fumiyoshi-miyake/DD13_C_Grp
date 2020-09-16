import os
import configparser


# 動作環境( 0:実機, 1:シュミレータ )
mode = 1

# デバッグ出力( OFF:0, ON:1 )
debug = 0

# センサー( 8×8:0, Lepton80×60:1 )
sensor = 1

# 顔検知( OFF:0, ON:1 )
face_detect = 1

# カラーグラデーション最小最大値
colorbar_min = 30.0
colorbar_max = 40.0

# 解像度( width, height )
resolution_width = 640
resolution_height = 480


# サーモグラフィ画像サイズ, 正方形,
thermo_height = 120
thermo_width = thermo_height

# カラーバー画像サイズ, 縦幅はサーモグラフィ画像に合わせる,
colorbar_width = 20
colorbar_height = thermo_height

# サーモグラフィ合成位置オフセット（画面左下端からの距離）
comp_ofst_x = 5
comp_ofst_y = resolution_height - thermo_height - comp_ofst_x - 20


