import os
import configparser


# サーモグラフィ画像サイズ, 正方形,
thermo_height = 100
thermo_width = thermo_height

# カラーバー画像サイズ, 縦幅はサーモグラフィ画像に合わせる,
colorbar_width = 20
colorbar_height = thermo_height

# 合成位置オフセット
comp_ofst_x = 20


if os.path.exists('Setting.ini'):
    config_ini = configparser.ConfigParser()
    config_ini.read('Setting.ini', encoding='utf-8')

    # 0:実機 1:シュミレーター
    mode = int(config_ini['Common']['mode'])

    #デバッグ出力　OFF:0　ON:1
    debug = int(config_ini['Common']['debug'])

    # カラーグラデーション最小最大値
    colorbar_min = float(config_ini['ThermoSetting']['colorbar_min'])
    colorbar_max = float(config_ini['ThermoSetting']['colorbar_max'])

    # 合成位置オフセット
    resolution_height = int(config_ini['CameraSetting']['resolution_height'])
    comp_ofst_y = resolution_height - thermo_height - comp_ofst_x
    
else:
    print('Setting.iniがありません')
    mode = 1
    debug = 0


    # カラーグラデーション最小最大値
    colorbar_min = 35.0
    colorbar_max = 37.5

    # 合成位置オフセット
    cmp_ofst_y = 480 - thermo_height - cmp_ofst_x


