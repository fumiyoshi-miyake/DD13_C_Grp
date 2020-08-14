# dispsim : 出力シミュレータ

import os
import cv2

# 初期表示用画像
START_IMAGE = 'start_image.jpg'

# 入力ファイルパスが表示できなかった場合に表示する画像
READ_ERR_IMAGE = 'read_err_image.jpg'

# 表示ウィンドウ名
WIN_NAME = 'dispsim'

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

  
  cv2.waitKey(1)  # 描画更新用 1msec

  return True


