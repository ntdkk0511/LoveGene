import socket
import time

# MMDAgentに接続
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 50001))

print("1: VISION_EYE_OK を送信")
print("2: VISION_EYE_NG を送信")
choice = input("送信する判定を選んでください (1 or 2): ")

if choice == "1":
    sock.sendall(b"VISION_EYE_OK\n")
elif choice == "2":
    sock.sendall(b"VISION_EYE_NG\n")

sock.close()