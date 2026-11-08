import struct
import mmap
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

#演習Ⅱの第1週 課題4 静止画を用いた顔検出を改変したものです
def intro1(cap):

    model_path = "./media/dldata/blaze_face_short_range.tflite"
    BaseOptions = mp.tasks.BaseOptions
    FaceDetector = mp.tasks.vision.FaceDetector
    FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
    RunningMode = mp.tasks.vision.RunningMode

    options = FaceDetectorOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=RunningMode.IMAGE,
        min_detection_confidence=0.5
    )

    with FaceDetector.create_from_options(options) as detector:
        while cap.isOpened():
            #mmdからメッセージを受け取る
            str = recv_message()

            key = cv2.waitKey(10)
            #'q'またはエスケープキーが入力されたらwhileの外へ出る
            if ( key==ord('q') ) or ( key==27 ) : #Unicodeに変換
                break

            #カメラから画像(フレーム)を取得しframeに代入
            ret, frame = cap.read()
            if not ret:
                continue
            #自分を映すことを想定して左右反転
            frame=cv2.flip(frame, 1)

            res_img  = frame.copy()

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #BGRをRGBに変換
            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            # ここで顔検出
            results = detector.detect(mp_img)

            height, width, ch = frame.shape

            if results.detections:
                for detection in results.detections:
                    print(detection)

                    # ★ バウンディングボックス（ピクセル座標） ★
                    bbox = detection.bounding_box
                    print('左上の座標', bbox.origin_x, bbox.origin_y)
                    print('バンディングボックスの大きさ', bbox.width, bbox.height)

                    # ★ キーポイント（0〜1の正規化座標） ★
                    r_eye = detection.keypoints[0]
                    l_eye = detection.keypoints[1]
                    nose  = detection.keypoints[2]
                    mouth = detection.keypoints[3]
                    r_ear = detection.keypoints[4]
                    l_ear = detection.keypoints[5]

                    print('右目の座標', r_eye.x*width, r_eye.y*height)
                    print('口の座標', int(mouth.x*width), int(mouth.y*height))

                    # ★ OpenCVで描画（旧 mp_drawing の代わり） ★
                    pt1 = (bbox.origin_x, bbox.origin_y)
                    pt2 = (bbox.origin_x + bbox.width, bbox.origin_y + bbox.height)
                    cv2.rectangle(res_img, pt1, pt2, color=(0, 128, 255), thickness=2)

                    cv2.circle(
                        res_img,
                        (int(nose.x*width), int(nose.y*height)),
                        8,
                        color=(0, 128, 255),
                        thickness=2
                    )

            cv2.imshow('MediaPipe Face Detection (Tasks API)', res_img)

            ########################ここに書く##########################
            #課題1：顔検出がされれば，MMDAgentに顔検出のメッセージを送る
            if results.detections: #1つ以上検出結果があれば
                send_message(b"face_detect")
                
                #↑のprint文を削除して，ここにコードを書く

     
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
        intro1(cap)
