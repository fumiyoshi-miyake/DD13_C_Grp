import time
import module
import setting



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
            print(pic)
#’Ctrl+C’を受け付けると終了
except KeyboardInterrupt:
    print("done")
