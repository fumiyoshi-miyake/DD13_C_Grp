# dispsim : 出力シミュレータ(実機のコードもここに含める)

import os
import cv2
import subprocess

# 初期表示用画像
START_IMAGE = 'start_image.jpg'

# 入力ファイルパスが表示できなかった場合に表示する画像
READ_ERR_IMAGE = 'read_err_image.jpg'

# 表示ウィンドウ名
WIN_NAME = 'dispsim'

# ------------------------------
# xrandr | grep '*'コマンドの実行（実機）
# ------------------------------
def command2pipe(cmd1, cmd2):
   p = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
   p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
   p.stdout.close()
   first_line, rest_lines = p2.communicate()
   return(first_line, rest_lines)

# ------------------------------
# 解像度の取得取得（実機）
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
# 表示ウィンドウ作成（実機）
# ------------------------------
def open_disp_machine():
  cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)
  #解像度取得
  widthPixel, heightPixel = getResolution()
  #表示ウィンドウを解像度のサイズに設定
  cv2.resizeWindow(WIN_NAME, int(widthPixel), int(heightPixel))
  #表示ウィンドウの座標を左上に移動する（タスクバーが表示する設定の場合は、タスクバーの下が原点になる）
  cv2.moveWindow(WIN_NAME, 0, 0)
  img = cv2.imread(START_IMAGE)
  cv2.imshow(WIN_NAME, img)
  return

# ------------------------------
# 表示ウィンドウ作成
# ------------------------------
def open_disp():
  cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)
  img = cv2.imread(START_IMAGE)
  cv2.imshow(WIN_NAME, img)
  return

# ------------------------------
# 表示ウィンドウを閉じる
# ------------------------------
def close_disp():
  #cv2.destroyWindow(WIN_NAME)
  cv2.destroyAllWindows()
  return

# ------------------------------
# 入力パラメータ：HDサイズのJPGファイル
# 機能　　　　　：画面に入力画像を出力する
# ------------------------------
def dispsim(img):
#  print('path = ' + jpg_path)  #forDebug

#  img = None

  # 入力パス存在確認
#  if not os.path.exists(jpg_path):
#    print('Not exist [ ' + jpg_path + ' ]')
#  else:
    # JPGファイル読み込み
#    img = cv2.imread(jpg_path)
  
  # 画像表示
  if img is None:
    # 指定パスの画像が表示できない場合は既定ファイルを読み込む
    img = cv2.imread(READ_ERR_IMAGE)
  
    if img is None:
      # 既定ファイルも開けなかった場合の処理（暫定）
      # 全てのウィンドウを閉じて終了
      cv2.destroyAllWindows()
      return False

  cv2.imshow(WIN_NAME, img)

  #キーボード入力1ms待ち(これないと画像表示されない)
  cv2.waitKey(1)  # 描画更新用 1msec

  prop_val = cv2.getWindowProperty(WIN_NAME, cv2.WND_PROP_ASPECT_RATIO)
  # 閉じるボタンが押された時の処理
  if prop_val < 0:
    cv2.destroyAllWindows()
    return False

  return True


