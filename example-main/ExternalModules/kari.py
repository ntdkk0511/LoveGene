
import cv2
import numpy as np
from deepface import DeepFace
import os
import time

img_path = r"C:\Users\kuato\OneDrive\デスクトップ\CGⅡ\media3_2026\test.png"

print(cv2.__file__)
print(cv2.data.haarcascades)

path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
print(os.path.exists(path))

# 日本語を含むパスから画像を読み込む
if not os.path.exists(img_path):
    print("画像ファイルが存在しません")
else:
    data = np.fromfile(img_path, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)

    if img is None:
        print("画像のデコードに失敗しました")
    else:
        print("画像の読み込みに成功しました")

    #results = DeepFace.analyze(
        #img,
        #actions=["age", "gender","emotion"],
        #detector_backend="retinaface"
    #)

    #print("分析結果:", results
    st = time.time()
    results = DeepFace.analyze(
        img,
        actions=["emotion"],
        detector_backend='opencv',
        enforce_detection=False
    )
    ft = time.time()
    print("表情:", results[0]["dominant_emotion"],ft-st)
