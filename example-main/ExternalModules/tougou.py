import cv2
import mediapipe as mp
import os
import time
import socket
import threading
import re
from deepface import DeepFace
import numpy as np
from dotenv import load_dotenv  # 環境変数読み込み用

# .env ファイルから環境変数をロード
load_dotenv()

# Google Gemini API 用ライブラリ
try:
    from google import genai
    from google.genai import types
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    print("【警告】google-genai がインストールされていません。'pip install google-genai' を実行してください。")

# ==================================================
# 設定項目
# ==================================================
HOST = '127.0.0.1'
PORT = 50000  # MMDAgent-EX のソケットポート番号

# 環境変数から Gemini API キーを取得
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ジェネ（恋愛マスター）のシステムプロンプト
SYSTEM_INSTRUCTION = """
あなたは恋愛相談マスターの3Dアバター「ジェネ」です。
ユーザーからの質問や雑談に対して、以下のルールを厳守して回答してください。

【ルール】
1. 明るくフレンドリーで親しみやすい口調（「〜だよ！」「〜してみよう！」など）で答えてください。
2. 音声合成ソフトが読み上げるため、1〜2文程度の簡潔で短めの文章にしてください。
3. 途中で文章が切れず、必ず句点（。）や感嘆符（！）まで完結した文章を作ってください。
4. 漢字の読み間違いを防ぐため、難解な漢字や絵文字・特殊記号は使わないでください。
"""

# ==================================================
# MMDAgent-EX ソケット通信＆自動再接続関数
# ==================================================
sock = None

def connect_mmd():
    """MMDAgent-EX へのソケット接続を行う"""
    global sock
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.0)
        s.connect((HOST, PORT))
        sock = s
        print("【接続成功】MMDAgent-EX に正常に接続しました。")
        return True
    except Exception as e:
        print(f"【注意】MMDAgent-EX 未接続: {e}")
        sock = None
        return False

# 初回接続
connect_mmd()

def send_to_mmd(text: str):
    """MMDAgent-EX へ発話コマンドと下部字幕表示コマンドを送信（切断時の自動再接続機能付き）"""
    global sock
    
    # 1. 音声合成発話コマンド
    synth_cmd = f"SYNTH_START|0|mei_voice_normal|{text}\n"
    
    # 2. 下部枠内に表示する字幕コマンド
    # CAPTION_START|識別名|スタイル|テキスト|文字サイズ|水平位置|垂直位置(0.0=下端, 1.0=上端)|表示フレーム数
    caption_cmd = f'CAPTION_START|gene_cap|_default|"{text}"|1.0|CENTER|0.1|300\n'
    
    # 2つのコマンドを結合してエンコード
    encoded_cmd = (synth_cmd + caption_cmd).encode("utf-8")

    # 接続がない場合は再接続を試みる
    if sock is None:
        if not connect_mmd():
            print("【送信スキップ】MMDAgent-EX との再接続に失敗しました。\n")
            return

    try:
        sock.sendall(encoded_cmd)
        print("【送信】発話および下部字幕メッセージを MMDAgent-EX へ送信しました。\n")
    except (socket.error, OSError) as se:
        print(f"【通信切断検知】ソケットが切断されていたため再接続を試みます: {se}")
        try:
            sock.close()
        except Exception:
            pass
        sock = None

        # 再接続して再送信
        if connect_mmd():
            try:
                sock.sendall(encoded_cmd)
                print("【再送信成功】発話および下部字幕メッセージを MMDAgent-EX へ送信しました。\n")
            except Exception as re_e:
                print(f"【再送信失敗】MMDAgent-EX への送信に失敗しました: {re_e}\n")
                sock = None

# Gemini クライアント初期化（15秒のタイムアウトを設定）
gemini_client = None
if HAS_GEMINI and GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options=types.HttpOptions(timeout=15000)  # 15秒でタイムアウト
        )
        print("【Gemini API】正常に初期化されました。")
    except Exception as e:
        print(f"【Gemini 初期化エラー】: {e}")
else:
    print("【注意】GEMINI_API_KEY が .env から読み込めなかったか設定されていません。")

# ==================================================
# LLM（Gemini）応答処理
# ==================================================
def ask_gemini_and_speak(user_text: str):
    """ユーザーの発話を受け取り、Gemini で回答を生成して MMDAgent-EX に喋らせる（非同期実行用）"""
    global gemini_client
    if not gemini_client:
        print("【LLMエラー】Gemini API キーが設定されていないか無効です。")
        return

    print(f"\n[LLM思考中...] ユーザー: {user_text}")
    
    # 1. Gemini API によるテキスト生成
    reply_text = ""
    max_retries = 2
    for attempt in range(1, max_retries + 1):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-3.8-flash",
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
        except Exception as e:
            err_msg = str(e)
            if ("503" in err_msg or "504" in err_msg or "UNAVAILABLE" in err_msg or "DEADLINE_EXCEEDED" in err_msg) and attempt < max_retries:
                print(f"【LLM混雑中/タイムアウト】サーバー高負荷のため再試行します ({attempt}/{max_retries})...")
                time.sleep(2)
            else:
                print(f"【LLM通信タイムアウト/エラー】: {e}")
                reply_text = "ごめんね、通信が混み合っていてうまく繋がらなかったよ。"
                break

    if not reply_text:
        reply_text = "ごめんね、うまく言葉がまとまらなかったよ。"

    # 2. Open_JTalk 用テキストクリーニング＆不完全文ガード
    reply_text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', reply_text)
    reply_text = reply_text.replace("〜", "ー").replace("~", "ー")
    reply_text = re.sub(r'[【】\[\]\(\)（）「」『』<>]', '', reply_text)
    
    # 最後の句点（。！？）まででカット、無ければ「。」を付与
    last_punct = max(reply_text.rfind("。"), reply_text.rfind("！"), reply_text.rfind("？"))
    if last_punct != -1:
        reply_text = reply_text[:last_punct + 1]
    else:
        reply_text += "。"

    if len(reply_text) < 6:
        reply_text = "相手がリラックスしている時に話しかけてみよう！"

    print(f"[ジェネの回答]: {reply_text}")

    # 3. MMDAgent-EX へ発話および字幕コマンドを送信
    send_to_mmd(reply_text)

def console_input_loop():
    """ターミナルからの入力を受付し、LLM呼出を完全非同期スレッドで起動"""
    time.sleep(2)
    print("\n==================================================")
    print("★ テキスト入力による LLM 応答テストが可能です。")
    print("   質問を入力して Enter を押すとジェネが喋ります。")
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

# ターミナル入力用スレッド起動
input_thread = threading.Thread(target=console_input_loop, daemon=True)
input_thread.start()

# ==================================================
# MediaPipe モデルファイルのパス自動設定
# ==================================================
base_dir = os.path.dirname(__file__)

candidates = [
    os.path.abspath(os.path.join(base_dir, "..", "..", "face_landmarker.task")),
    os.path.abspath(os.path.join(base_dir, "..", "face_landmarker.task")),
    os.path.abspath(os.path.join(base_dir, "face_landmarker.task"))
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

# ==================================================
# 表情解析の非同期処理
# ==================================================
ang = dis = fea = hap = sad = sur = neu = su = 0
is_analyzing_emotion = False

def analyze_emotion_async(frame_img):
    global ang, dis, fea, hap, sad, sur, neu, su, is_analyzing_emotion
    try:
        analysis = DeepFace.analyze(
            frame_img, 
            actions=['emotion'],
            detector_backend='opencv',
            enforce_detection=False
        )
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
    finally:
        is_analyzing_emotion = False

# ==================================================
# メイン処理ループ（視線・描画）
# ==================================================
cap = cv2.VideoCapture(0)
start = last = time.monotonic()
front_seconds = off_seconds = 0.0
frame_number = 0
gaze_state = False

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
            frame_number += 1
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

            # 表情解析を完全非同期スレッドでバックグラウンド実行（30フレームに1回）
            if frame_number % 30 == 0 and not is_analyzing_emotion:
                is_analyzing_emotion = True
                threading.Thread(
                    target=analyze_emotion_async, 
                    args=(frame.copy(),), 
                    daemon=True
                ).start()

            cv2.imshow("show", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                if su > 0:
                    print("\n--- 表情計測割合 ---")
                    print("怒り:", round(ang * 100 / su, 1), "%")
                    print("嫌悪:", round(dis * 100 / su, 1), "%")
                    print("恐怖:", round(fea * 100 / su, 1), "%")
                    print("喜び:", round(hap * 100 / su, 1), "%")
                    print("悲しみ:", round(sad * 100 / su, 1), "%")
                    print("驚き:", round(sur * 100 / su, 1), "%")
                    print("普通:", round(neu * 100 / su, 1), "%")
                break

except KeyboardInterrupt:
    print("\n【終了処理】プログラムを終了します。")

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