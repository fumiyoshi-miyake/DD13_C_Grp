import os
import configparser

if os.path.exists('Setting.ini'):
    config_ini = configparser.ConfigParser()
    config_ini.read('Setting.ini', encoding='utf-8')

    # 0:実機 1:シュミレーター
    mode = int(config_ini['Common']['mode'])

    #デバッグ出力　OFF:0　ON:1
    debug = int(config_ini['Common']['debug'])
else:
    print('Setting.iniがありません')
    mode = 1
    debug = 0