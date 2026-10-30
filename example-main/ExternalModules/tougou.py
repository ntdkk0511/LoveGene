import cv2
import mediapipe as mp
import os
import time
import socket  # MMDAgent-EX 通信用

from deepface import DeepFace
import numpy as np

# ==================================================
# MMDAgent-EX ソケット通信設定
# ==================================================
HOST = '127.0.0.1'
PORT = 50000  # MMDAgent-EX のソケットポート番号

sock = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    sock = s
    print("【接続成功】MMDAgent-EX に正常に接続しました。")
except Exception as e:
    print(f"【注意】MMDAgent-EX 未接続: {e}")
    print("※MMDAgent-EX を先に起動してから実行すると顔認識イベントが送信されます。")

# ==================================================
# モデルファイルのパス自動設定
# ==================================================
base_dir = os.path.dirname(__file__)

candidates = [
    os.path.abspath(os.path.join(base_dir, "..", "..", "face_landmarker.task")), # 2つ上
    os.path.abspath(os.path.join(base_dir, "..", "face_landmarker.task")),       # 1つ上
    os.path.abspath(os.path.join(base_dir, "face_landmarker.task"))              # 同階層
]

MODEL_PATH = None
for path in candidates:
    if os.path.exists(path):
        MODEL_PATH = path
        break

if MODEL_PATH is None:
    print("\n[エラー] face_landmarker.task が見つかりませんでした。")
    exit(1)

print(f"【モデル読み込み】{MODEL_PATH}")

with open(MODEL_PATH, "rb") as f:
    model_data = f.read()

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker

options = mp.tasks.vision.FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_buffer=model_data),
    running_mode=mp.tasks.vision.RunningMode.VIDEO,
    num_faces=1
)

EYES = [
    (33, 133, 159, 145, 468),
    (362, 263, 386, 374, 473)
]

##############################
X_MIN, X_MAX = 0.42, 0.55
Y_MIN, Y_MAX = 0.42, 0.55
##############################

def get_eye_position(landmarks, eye):
    left, right, top, bottom, iris = eye
    l, r = landmarks[left], landmarks[right]
    t, b = landmarks[top], landmarks[bottom]
    i = landmarks[iris]

    width = abs(r.x - l.x)
    height = abs(b.y - t.y)

    if width < 0.001 or height < 0.001:
        return None

    x = (i.x - min(l.x, r.x)) / width
    y = (i.y - min(t.y, b.y)) / height
    return x, y


def judge_gaze(x, y):
    return X_MIN <= x <= X_MAX and Y_MIN <= y <= Y_MAX


cap = cv2.VideoCapture(0)
start = last = time.monotonic()
front_seconds = off_seconds = 0.0
frame_number = 0

ang = 0
dis = 0
fea = 0
hap = 0
sad = 0
sur = 0
neu = 0
su = 0

gaze_state = False
greet_sent = False  # イベント連送を防止するため、初回送信済みフラグを追加

try:
    with FaceLandmarker.create_from_options(options) as landmarker:
        while True:
            ret, frame = cap.read()
            now = time.monotonic()

            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            timestamp = max(int((now - start) * 1000), frame_number)
            frame_number = timestamp + 1
            result = landmarker.detect_for_video(image, timestamp)

            detected_front = None

            if result.face_landmarks:
                # --- 顔認識時に MMDAgent-EX へイベント送信（初回1回のみ）---
                if sock is not None and not greet_sent:
                    try:
                        sock.sendall(b"FACE_DETECTED\n")
                        print("【送信】顔を認識したため FACE_DETECTED を送信しました。")
                        greet_sent = True  # 1回送信したらフラグを立てて連送を防止
                    except Exception as e:
                        print(f"送信エラー（切断されました）: {e}")
                        try:
                            sock.close()
                        except Exception:
                            pass
                        sock = None  # 切断後はソケットをクリアしてログ連打を防止

                landmarks = result.face_landmarks[0]
                positions = []

                for eye in EYES:
                    pos = get_eye_position(landmarks, eye)
                    if pos is not None:
                        positions.append(pos)

                    p = landmarks[eye[4]]
                    cv2.circle(frame, (int(p.x * w), int(p.y * h)),
                               4, (0, 255, 0), -1)

                if positions:
                    x = sum(p[0] for p in positions) / len(positions)
                    y = sum(p[1] for p in positions) / len(positions)
                    detected_front = judge_gaze(x, y)

            dt = now - last
            last = now

            if detected_front is not None:
                gaze_state = detected_front

            if gaze_state:
                front_seconds += dt
            else:
                off_seconds += dt

            #############################################################
            ###### 表情解析 ######
            #############################################################
            analysis = DeepFace.analyze(frame, 
                                  actions=['emotion'],
                                  detector_backend='opencv',
                                  enforce_detection=False)

            if len(analysis) > 0:
                emotion = analysis[0]["dominant_emotion"]

                if emotion == "angry":
                    ang += 1
                elif emotion == "disgust":
                    dis += 1
                elif emotion == "fear":
                    fea += 1
                elif emotion == "happy":
                    hap += 1
                elif emotion == "sad":
                    sad += 1
                elif emotion == "surprise":
                    sur += 1
                elif emotion == "neutral":
                    neu += 1
                su += 1

            cv2.imshow("show", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                if su > 0:
                    ang_w = ang * 100 / su
                    dis_w = dis * 100 / su
                    fea_w = fea * 100 / su
                    hap_w = hap * 100 / su
                    sad_w = sad * 100 / su
                    sur_w = sur * 100 / su
                    neu_w = neu * 100 / su
                    print("")
                    print("---表情---")
                    print("怒り:", round(ang_w, 1), "%")
                    print("嫌悪:", round(dis_w, 1), "%")
                    print("恐怖:", round(fea_w, 1), "%")
                    print("喜び:", round(hap_w, 1), "%")
                    print("悲しみ:", round(sad_w, 1), "%")
                    print("驚き:", round(sur_w, 1), "%")
                    print("普通:", round(neu_w, 1), "%")
                break

finally:
    cap.release()
    cv2.destroyAllWindows()
    if sock:
        try:
            sock.close()
        except Exception:
            pass

    total = front_seconds + off_seconds
    print("\n--- 最終計測結果 ---")
    print(f"正面:      {front_seconds:.2f}秒")
    print(f"正面以外: {off_seconds:.2f}秒")

    if total > 0:
        print(f"正面の割合:      {front_seconds / total * 100:.1f}%")
        print(f"正面以外の割合:  {off_seconds / total * 100:.1f}%")
    else:
        print("計測時間が短いため、割合を計算できません。")