import subprocess as sub
import sys
import mmap

import struct
import numpy as np
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import mediapipe as mp

#この部分はMMDAgentとの通信部分です．触らないでください
def recv_message():
    len = mm.find(b'\x00',0x00,0xff)
    str = ''
    if len !=0 :	
        mm.seek(0x0)
        line = mm.read(len)
        try:
            str = line.decode()
        except UnicodeDecodeError:
            print("Decode Error")
        mm.seek(0x0)
        mm.write(b'\x00')
    return str

def send_message(send):
    mm.seek(0x200)
    mm.write(struct.pack('512s', send))
#ここまではMMDAgentとの通信部分です．触らないでください

def intro2(cap):
    while True:
        #mmdからメッセージを受け取る
        key = cv2.waitKey(1) & 0xFF
        #'q'またはエスケープキーが入力されたらwhileの外へ出る
        if ( key==ord('w') ) : #Unicodeに変換
            break

        window = np.zeros((200, 400, 3), dtype=np.uint8)
        cv2.imshow("input image",window)

        ########################ここに書く##########################
        
        #課題3：キーボードの0が押されれば，MMDAgentにkeyboard_0の
        #文字列を送る
        if(key == ord("0")):
            send_message(b"keyboard_0")
            #cv2.putText(window,f"k",(30, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),1)

        #課題4：MMDAgentの発話内容を表示する
        msg = recv_message()
        #print(msg)

        #課題5：MMDAgentの発話に「こんにちは」が含まれている場合
        #「こんにちはが発話されました」を表示する
        if "キーボード" in msg:
            #cv2.putText(window,f"k",(30, 100),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),1)
            #cv2.imshow("input image",window)
            sub.run([sys.executable,"./example-main./ExternalModules./sisen.py"])
        
        #mmdからメッセージを受け取る
        #str = recv_message()

       


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    #カメラ画像の解像度を指定
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    #共有メモリのオープン
    mm = mmap.mmap(-1, 0x400, "Share_MMD_Camera")

    if(cap.isOpened()==True):
        intro2(cap)

    

    #sub.run([sys.executable,"./example-main./ExternalModules./tougou.py"])