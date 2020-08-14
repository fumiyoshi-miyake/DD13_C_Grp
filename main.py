import time
import module
import setting
from dispsim import *


if setting.debug:
  print('start dispsim ---')

  # ウィンドウ開く
  open_disp()
  
try:
     while(True):
        #0.1秒のスリープ
        time.sleep(.1)
        #時間表示
        print(time.time())
        temp = module.readTemp()
        if setting.debug:
            print(temp)

        pic = module.readPic()
        if setting.debug:
            #画像出力
            dispsim(pic)

#’Ctrl+C’を受け付けると終了
except KeyboardInterrupt:
    print("done")

if setting.debug:
    close_disp()
