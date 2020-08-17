# -*- coding: utf-8 -*-
import sys
import configparser
import picamera
import picamera.array

def InitCamera( debug ):
    # カメラ初期化
    camera = picamera.PiCamera()

    config_ini = configparser.ConfigParser()
    config_ini.read('Setting.ini', encoding='utf-8')

    # 解像度
    str_width = config_ini['CameraSetting']['resolution_width']
    str_height = config_ini['CameraSetting']['resolution_height']
    if str_width.isdecimal() and str_height.isdecimal():
        width = int(str_width)
        height = int(str_height)
        if debug:
            print("resolution(%i,%i)" % (width, height))
        camera.resolution = (width, height)
    else:
        print("Warning : resolution(%s,%s)" % (str_width,str_height))

    #シャープネス
    param = config_ini['CameraSetting']['sharpness']
    if param.isdecimal():
        sharpness = int(param)
        if debug:
            print("sharpness=%i" % sharpness)
        camera.sharpness = sharpness
    else:
        print("Warning : sharpness=%s" % param)

    #コントラスト
    param = config_ini['CameraSetting']['contrast']
    if param.isdecimal():
        contrast = int(param)
        if debug:
            print("contrast=%i" % contrast)
        camera.contrast = contrast
    else:
        print("Warning : contrast=%s" % param)

    # 輝度
    param = config_ini['CameraSetting']['brightness']
    if param.isdecimal():
        brightness = int(param)
        if debug:
            print("brightness=%i" % brightness)
        camera.brightness = brightness
    else:
        print("Warning : brightness=%s" % param)

    #彩度
    param = config_ini['CameraSetting']['saturation']
    if param.isdecimal():
        saturation = int(param)
        if debug:
            print("saturation=%i" % saturation)
        camera.saturation = saturation
    else:
        print("Warning : saturation=%s" % param)

    # 感度(ISO)
    param = config_ini['CameraSetting']['ISO']
    if param.isdecimal():
        ISO = int(param)
        if debug:
            print("ISO=%i" % ISO)
        camera.iso = ISO
    else:
        print("Warning : ISO=%s" % param)

    # 手振れ補正
    video_stabilization = config_ini['CameraSetting']['video_stabilization']
    if video_stabilization == 'True':
        if debug:
            print("video_stabilization=True")
        camera.video_stabilization = True
    else:
        if debug:
            print("video_stabilization=False")
        camera.video_stabilization = False

    # 露光補正
    param = config_ini['CameraSetting']['exposure_compensation']
    if param.isdecimal():
        exposure_compensation = int(param)
        if debug:
            print("exposure_compensation=%i" % exposure_compensation)
        camera.exposure_compensation = exposure_compensation
    else:
        print("Warning : exposure_compensation=%s" % param)

    # 露出モード
    exposure_mode = config_ini['CameraSetting']['exposure_mode']
    if debug:
        print("exposure_mode=%s" % exposure_mode)
    camera.exposure_mode = exposure_mode

    # カメラの計測モード
    meter_mode = config_ini['CameraSetting']['meter_mode']
    if debug:
        print("meter_mode=%s" % meter_mode)
    camera.meter_mode = meter_mode

    # ホワイトバランス
    awb_mode = config_ini['CameraSetting']['awb_mode']
    if debug:
        print("awb_mode=%s" % awb_mode)
    camera.awb_mode = awb_mode

    # エフェクト
    image_effect = config_ini['CameraSetting']['image_effect']
    if debug:
        print("image_effect=%s" % image_effect)
    camera.image_effect = image_effect

    # カラーエフェクト
    color_effects = config_ini['CameraSetting']['color_effects']
    if debug:
        print("color_effects=%s" % color_effects)
    camera.color_effects = None

    # 画像回転
    param = config_ini['CameraSetting']['rotation']
    if param.isdecimal():
        rotation = int(param)
        if debug:
            print("rotation=%i" % rotation)
        camera.rotation = rotation
    else:
        print("Warning : rotation=%s" % param)

    # 水平方向反転
    hflip = config_ini['CameraSetting']['hflip']
    if hflip == 'True':
        if debug:
            print("hflip=True")
        camera.hflip = True
    else:
        if debug:
            print("hflip=False")
        camera.hflip = False

    # 垂直方向反転
    vflip = config_ini['CameraSetting']['vflip']
    if vflip == 'True':
        if debug:
            print("vflip=True")
        camera.vflip = True
    else:
        if debug:
            print("vflip=False")
        camera.vflip = False

    return camera

#if __name__ == "__main__":
#    InitCamera()
