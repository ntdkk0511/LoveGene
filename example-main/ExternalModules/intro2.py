import struct
import mmap
import numpy as np
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import mediapipe as mp
#ARマーカーを使用する場合は次の行を追加します
from cv2 import aruco

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
    #ARマーカーの設定
    dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_6X6_100) 
    parameters = aruco.DetectorParameters()

    while cap.isOpened():
        #mmdからメッセージを受け取る
        str = recv_message()
        key = cv2.waitKey(10)
        #'q'またはエスケープキーが入力されたらwhileの外へ出る
        if ( key==ord('q') ) or ( key==27 ) : #Unicodeに変換
            break

        #カメラから画像(フレーム)を取得しframeに代入
        ret, frame = cap.read()
        #マーカーを使用するときは左右反転不可
        #frame=cv2.flip(frame, 1)

        #ARマーカーを読み込むためグレースケールにする
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        #ARマーカーの検出
        detector = aruco.ArucoDetector(dict_aruco, parameters)
        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)

        #検出したマーカーにidと枠を描画
        result = aruco.drawDetectedMarkers(frame, corners, ids)

        #マーカー描画結果を表示
        cv2.imshow("input image",result)

        #検出されたマーカーの番号を1次元リストに格納する
        list_ids = np.ravel(ids)
        #print(ids)
        
        #マーカーの4隅の座標を表示する
        #print(corners)

        ########################ここに書く##########################
        #課題2：ID0のマーカーが検出されれば，MMDAgentにmarker_id0の
        #文字列を送る
        if list_ids ==  0:
            send_message(b"marker_id0")

        #課題3：キーボードの0が押されれば，MMDAgentにkeyboard_0の
        #文字列を送る
        if(key == ord("0")):
            send_message(b"keyboard_0")

        #課題4：MMDAgentの発話内容を表示する
        msg = recv_message()
        print(msg)

        #課題5：MMDAgentの発話に「こんにちは」が含まれている場合
        #「こんにちはが発話されました」を表示する
        if "こんにちは" in msg:
            print("こんにちはが発話されました")
        
        #mmdからメッセージを受け取る
        #str = recv_message()

        if 0 in list_ids :
            print("")
    
        #ここにコードを書く

        

     
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
        intro2(cap)
