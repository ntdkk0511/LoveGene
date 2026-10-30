import cv2
import socket
import time

# MMDAgent-EX の接続先設定
HOST = '127.0.0.1'
PORT =  50000 # MMDAgent-EXのソケットポート番号

def main():
    # OpenCVの標準顔検出モデルを読み込み
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Webカメラのオープン (0番カメラ)
    cap = cv2.VideoCapture(0)
    
    # MMDAgent-EX へのソケット接続
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print("MMDAgent-EX に正常に接続しました。")
    except Exception as e:
        print(f"MMDAgent-EX への接続エラー: {e}")

    face_detected_sent = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 顔検出の精度向上のためグレースケール化
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # 顔が認識された場合
        if len(faces) > 0:
            if not face_detected_sent and sock:
                # MMDAgent-EX へ送信するメッセージ
                message = "FACE_DETECTED\n"
                sock.sendall(message.encode('utf-8'))
                print("顔を認識しました。初期挨拶メッセージを送信します。")
                face_detected_sent = True
        else:
            # 画面から顔が外れたら再検知可能にする
            face_detected_sent = False

        # 'q' キーを押すと終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    if sock:
        sock.close()

if __name__ == '__main__':
    main()