import mmap
import struct
import numpy as np
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import mediapipe as mp
import time
import socket
import threading
import re
from deepface import DeepFace
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# .env ファイルから環境変数をロード
load_dotenv()

# Google Gemini API 用ライブラリ
try:
    from google import genai
    from google.genai import types
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    print("【警告】google-genai がインストールされていません。")

# ==================================================
# 通信・初期化処理 (mmap & Socket)
# ==================================================
HOST = '127.0.0.1'
PORT = 50000
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 共有メモリ (mmap) のオープン
mm = None
try:
    mm = mmap.mmap(-1, 0x400, "Share_MMD_Camera")
    print("【共有メモリ】Share_MMD_Camera に接続しました。")
except Exception as e:
    print(f"【注意】共有メモリオープン失敗: {e}")

def recv_message():
    """mmap 経由でのメッセージ受信"""
    if mm is None:
        return ""
    try:
        length = mm.find(b'\x00', 0x00, 0xff)
        msg_str = ''
        if length != 0:
            mm.seek(0x0)
            line = mm.read(length)
            try:
                msg_str = line.decode('utf-8', errors='ignore')
            except Exception:
                pass
            mm.seek(0x0)
            mm.write(b'\x00')
        return msg_str
    except Exception:
        return ""

def send_message(send_bytes: bytes):
    """mmap 経由での判定イベント送信"""
    if mm is None:
        return
    try:
        mm.seek(0x200)
        mm.write(struct.pack('512s', send_bytes))
    except Exception as e:
        print(f"【mmap送信エラー】: {e}")

# Socket 通信
sock = None
def connect_mmd():
    global sock
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect((HOST, PORT))
        sock = s
        print("【Socket接続】MMDAgent-EX に接続しました。")
        return True
    except Exception:
        sock = None
        return False

connect_mmd()

def send_to_mmd(text: str):
    """Gemini回答等の Socket 発話送信"""
    global sock
    synth_cmd = f"SYNTH_START|0|mei_voice_normal|{text}\n"
    caption_cmd = f'CAPTION_START|gene_cap|_default|"{text}"|1.0|CENTER|0.1|300\n'
    encoded_cmd = (synth_cmd + caption_cmd).encode("utf-8")

    if sock is None and not connect_mmd():
        return
    try:
        sock.sendall(encoded_cmd)
    except Exception:
        sock = None

# Gemini クライアント初期化
gemini_client = None
if HAS_GEMINI and GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options=types.HttpOptions(timeout=15000)
        )
        print("【Gemini API】正常に初期化されました。")
    except Exception as e:
        print(f"【Gemini 初期化エラー】: {e}")

SYSTEM_INSTRUCTION = """
あなたは恋愛相談マスターの3Dアバター「ジェネ」です。
明るくフレンドリーな口調（1〜2文程度の簡潔な文章）で回答してください。
"""

def ask_gemini_and_speak(user_text: str):
    global gemini_client
    if not gemini_client:
        return
    print(f"\n[LLM思考中...] ユーザー: {user_text}")
    reply_text = ""
    for attempt in range(1, 3):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-1.5-flash",
                contents=user_text,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.7,
                    max_output_tokens=200,
                ),
            )
            if response and response.text:
                reply_text = response.text.strip().replace("\n", " ").replace("\r", "")
            break
        except Exception:
            if attempt < 2:
                time.sleep(2)
            else:
                reply_text = "ごめんね、通信が混み合っていてうまく繋がらなかったよ。"

    if not reply_text:
        reply_text = "ごめんね、うまく言葉がまとまらなかったよ。"

    reply_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', reply_text)
    reply_text = reply_text.replace("〜", "ー").replace("~", "ー")
    reply_text = re.sub(r'[【】\[\]\(\)（）「」『』<>]', '', reply_text)
    
    last_punct = max(reply_text.rfind("。"), reply_text.rfind("！"), reply_text.rfind("？"))
    if last_punct != -1:
        reply_text = reply_text[:last_punct + 1]
    else:
        reply_text += "。"

    print(f"[ジェネの回答]: {reply_text}")
    send_to_mmd(reply_text)

def console_input_loop():
    time.sleep(2)
    print("\n==================================================")
    print("★ テキスト入力による LLM 応答テストが可能です。")
    print("==================================================\n")
    while True:
        try:
            user_input = input()
            if user_input.strip():
                threading.Thread(
                    target=ask_gemini_and_speak, 
                    args=(user_input.strip(),), 
                    daemon=True
                ).start()
        except (EOFError, KeyboardInterrupt):
            break

threading.Thread(target=console_input_loop, daemon=True).start()

# ==================================================
# グラフ画像出力関数
# ==================================================
def create_graph(data, colors, title, filename):
    plt.rcParams["font.family"] = "Meiryo"
    fig = plt.figure(figsize=(12.8, 7.2), dpi=100)
    fig.patch.set_alpha(0)

    bg = fig.add_axes([0.64, 0.57, 0.35, 0.39])
    bg.set_facecolor("white")
    bg.patch.set_edgecolor("#CCCCCC")
    bg.patch.set_linewidth(1.5)
    bg.set_xticks([])
    bg.set_yticks([])
    bg.set_zorder(0)

    ax = fig.add_axes([0.70, 0.63, 0.27, 0.25])
    ax.set_facecolor("none")
    ax.set_zorder(1)

    bars = ax.barh(
        list(data.keys()), list(data.values()),
        color=colors, height=0.5
    )

    ax.set_xlim(0, 100)
    ax.set_title(title, color="black", loc="left")
    ax.tick_params(colors="black")
    ax.grid(axis="x", alpha=0.25)
    ax.set_axisbelow(True)

    for bar, value in zip(bars, data.values()):
        ax.text(
            value + 2,
            bar.get_y() + bar.get_height()/2,
            f"{value}%",
            color="black",
            va="center"
        )

    for spine in ax.spines.values():
        spine.set_visible(False)

    base_dir = os.path.dirname(__file__)
    target_dir = os.path.abspath(os.path.join(base_dir, "..", "Scenarios", "QandA"))
    if not os.path.exists(target_dir):
        target_dir = base_dir

    save_path = os.path.join(target_dir, filename + ".png")
    plt.savefig(
        save_path,
        dpi=100,
        transparent=False,
        facecolor="none"
    )
    plt.close()

# ==================================================
# MediaPipe & 解析・評価ルーチン
# ==================================================
base_dir = os.path.dirname(__file__)
candidates = [
    os.path.abspath(os.path.join(base_dir, "..", "..", "face_landmarker.task")),
    os.path.abspath(os.path.join(base_dir, "..", "face_landmarker.task")),
    os.path.abspath(os.path.join(base_dir, "face_landmarker.task"))
]

MODEL_PATH = next((p for p in candidates if os.path.exists(p)), None)
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

X_MIN, X_MAX = 0.42, 0.55
Y_MIN, Y_MAX = 0.42, 0.55

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

def sisen_s(cap):
    """「言ってみて」受信からの計測・評価メインループ"""
    print("【計測開始】視線および表情の解析を実行中...")
    start = last = time.monotonic()
    front_seconds = off_seconds = 0.0
    frame_number = 0
    gaze_state = False

    ang = dis = fea = hap = sad = sur = neu = su = 0

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
                    cv2.circle(frame, (int(p.x * w), int(p.y * h)), 4, (0, 255, 0), -1)

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

            # 表情解析 (DeepFace)
            try:
                analysis = DeepFace.analyze(frame, actions=['emotion'], detector_backend='opencv', enforce_detection=False)
                if len(analysis) > 0:
                    emotion = analysis[0]["dominant_emotion"]
                    if emotion == "angry": ang += 1
                    elif emotion == "disgust": dis += 1
                    elif emotion == "fear": fea += 1
                    elif emotion == "happy": hap += 1
                    elif emotion == "sad": sad += 1
                    elif emotion == "surprise": sur += 1
                    elif emotion == "neutral": neu += 1
                    su += 1
            except Exception:
                pass

            # 「おつかれさま」受信で計測終了
            msg = recv_message()
            if "おつかれさま" in msg:
                print("【計測終了】「おつかれさま」を受信しました。")
                break

    # 結果集計とグラフ保存
    total = front_seconds + off_seconds
    if total <= 0: total = 1.0
    if su <= 0: su = 1

    ang_w = ang * 100 / su
    dis_w = dis * 100 / su
    fea_w = fea * 100 / su
    hap_w = hap * 100 / su
    sad_w = sad * 100 / su
    sur_w = sur * 100 / su

    gaze_result = {"正面": round(front_seconds / total * 100, 1), "正面以外": round(off_seconds / total * 100, 1)}
    emotion_result = {
        "喜び": round(hap_w, 1), "嫌悪": round(dis_w, 1), "怒り": round(ang_w, 1),
        "悲しみ": round(sad_w, 1), "驚き": round(sur_w, 1), "恐怖": round(fea_w, 1)
    }

    create_graph(emotion_result, ["#36D6E7", "#A78BFA", "#FF7373", "#F5B942", "#6EE7A0", "#41F750"], "表情評価", "result_h")
    create_graph(gaze_result, ["#36D6E7", "#FF9B71"], "視線評価", "result_s")
    print("【評価完了】result_h.png および result_s.png を生成しました。")

    # シナリオ側からの問い合わせに応じた評価イベント送信
    while True:
        msg = recv_message()
        if "表情" in msg:
            time.sleep(2)
            happy_w = round(hap_w, 1)
            if happy_w > 80:
                send_message(b"verygood_h")
            elif happy_w > 50:
                send_message(b"good_h")
            else:
                send_message(b"bad_h")

        if "視線" in msg:
            time.sleep(2)
            front_s_w = front_seconds / total * 100
            if front_s_w > 80:
                send_message(b"verygood_s")
            elif front_s_w > 50:
                send_message(b"good_s")
            else:
                send_message(b"bad_s")
            break
        time.sleep(0.1)

# ==================================================
# メインループ
# ==================================================
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # 既存のグラフ画像削除
    target_folder = os.path.abspath(os.path.join(base_dir, "..", "Scenarios", "QandA"))
    for file in ["result_h.png", "result_s.png"]:
        path = os.path.join(target_folder, file)
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

    print("【待機中】「言ってみて」のメッセージを受信待ち...")
    try:
        if cap.isOpened():
            while True:
                msg = recv_message()
                if "言ってみて" in msg:
                    sisen_s(cap)
                    print("【完了】待機状態に戻ります。")
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n【終了】プログラムを終了します。")
    finally:
        cap.release()
        cv2.destroyAllWindows()