import os
import cv2
import mediapipe as mp
import os
import time
import numpy as np

# cap = cv2.VideoCapture(0)
# cnt = 0

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # 文字表示用のウィンドウ画像を作成
#     window = np.zeros((200, 400, 3), dtype=np.uint8)

#     if cnt < 3:
#         print("a")
#         cnt += 1

#     # ウィンドウに文字を表示
#     cv2.putText(
#         window,
#         f"cnt = {cnt}",
#         (30, 100),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         1,
#         (0, 255, 0),
#         2
#     )

#     cv2.imshow("Real Time Analysis", frame)
#     cv2.imshow("Output", window)

#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "face_landmarker.task")
)

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

            cv2.imshow("Gaze Measurement", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

finally:
    cap.release()
    cv2.destroyAllWindows()

    while True:
        window = np.zeros((200, 400, 3), dtype=np.uint8)
        total = front_seconds + off_seconds
        cv2.putText(window,f"front:      {front_seconds:.2f}s",(30, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),1)
        cv2.putText(window,f"off front: {off_seconds:.2f}s",(30, 100),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),1)
        cv2.putText(window,f"front(%):      {front_seconds / total * 100:.1f}%",(30, 150),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),1)
        cv2.putText(window,f"off front(%): {off_seconds / total * 100:.1f}%",(30, 200),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),1)



        cv2.imshow("Output", window)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('f'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # print("\n--- 最終計測結果 ---")
    # print(f"正面:      {front_seconds:.2f}秒")
    # print(f"正面以外: {off_seconds:.2f}秒")

    # if total > 0:
    #     print(f"正面の割合:      {front_seconds / total * 100:.1f}%")
    #     print(f"正面以外の割合:  {off_seconds / total * 100:.1f}%")
    # else:
    #     print("計測時間が短いため、割合を計算できません。")