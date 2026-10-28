import struct
import mmap
import numpy as np
import cv2
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
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

def sample(cap):
    #カメラが開いている間ずっと
    while cap.isOpened():

        #カメラから画像(フレーム)を取得しframeに代入
        ret, frame = cap.read()
        #自分を映すことを想定して左右反転
        frame=cv2.flip(frame, 1)

        #mmdからメッセージを受け取る
        str = recv_message()
        if len(str) > 0:
            print(str)

        #現在のフレームを表示
        cv2.imshow("input image",frame)
        key = cv2.waitKey(1)

        if key == ord('0'):
            send_message(b'keyboard_0')
        if key == ord('q'):
            break    

if __name__ == '__main__':
    #カメラを取得
    #カメラが1つしかなければ0を引数として設定
    #カメラが2つの場合(例：内蔵カメラとUSBカメラ)0または1を設定
    cap = cv2.VideoCapture(0)
    #カメラ画像の解像度を指定
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    #共有メモリのオープン
    mm = mmap.mmap(-1, 0x400, "Share_MMD_Camera")

    if(cap.isOpened()==True):
        #カメラ画像をキャプチャして表示するだけ
        sample(cap)
