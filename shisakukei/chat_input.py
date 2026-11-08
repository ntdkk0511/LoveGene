import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket

HOST = "127.0.0.1"
PORT = 50001

def send_to_gene(reply):
    command = f"SYNTH_START|0|mei_voice_normal|{reply}\n"

    try:
        with socket.create_connection((HOST, PORT), timeout=3) as client:
            client.sendall(command.encode("utf-8"))
        return True
    except OSError as e:
        messagebox.showerror(
            "接続エラー",
            f"MMD-Agent EXに接続できません。\n{e}"
        )
        return False

def get_reply(message):
    if "好き" in message:
        return "ありがとう。とても嬉しいよ！"
    elif "ご飯" in message or "デート" in message:
        return "いいね！楽しそう！"
    elif "こんにちは" in message:
        return "こんにちは！今日はどうしたの？"
    else:
        return "うん、もう少し詳しく聞かせて！"

def send_message(event=None):
    message = entry.get().strip()

    if not message:
        return

    reply = get_reply(message)

    chat.insert(tk.END, f"あなた：{message}\n")
    chat.insert(tk.END, f"Gene：{reply}\n\n")
    chat.see(tk.END)
    entry.delete(0, tk.END)

    send_to_gene(reply)

root = tk.Tk()
root.title("Geneとのチャット")
root.geometry("450x450")

chat = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Yu Gothic UI", 11)
)
chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
chat.configure(state="disabled")

entry = tk.Entry(root, font=("Yu Gothic UI", 12))
entry.pack(fill=tk.X, padx=10, pady=10)

def submit(event=None):
    chat.configure(state="normal")
    send_message()
    chat.configure(state="disabled")

entry.bind("<Return>", submit)
entry.focus_set()

root.mainloop()
