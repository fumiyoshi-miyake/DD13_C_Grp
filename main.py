import time

try:
     while(True):
        #0.1秒のスリープ
        time.sleep(.1)
        #時間表示
        print(time.time())

#’Ctrl+C’を受け付けると終了
except KeyboardInterrupt:
    print("done")
