import os
from google import genai
from google.genai import types

# --------------------------------------------------
# 初期設定
# --------------------------------------------------
# ここに取得した Gemini の API キーを貼り付けます
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

client = genai.Client(api_key=GEMINI_API_KEY)

# ジェネのキャラクター・発話ルール設定
SYSTEM_INSTRUCTION = """
あなたは恋愛相談マスターの3Dアバター「ジェネ」です。
ユーザーからの質問や雑談に対して、以下のルールを厳守して回答してください。

【ルール】
1. 明るくフレンドリーで親しみやすい口調（「〜だよ！」「〜してみよう！」など）で答えてください。
2. 音声合成ソフト（Open_JTalk）が読み上げるため、1〜2文程度の簡潔で短めの文章にしてください。
3. 漢字の読み間違いを防ぐため、難解な漢字や特殊な記号（絵文字、顔文字、カッコなど）は使わないでください。
"""

def generate_llm_response(user_text: str) -> str:
    """ユーザーのテキストを受け取り、Gemini でジェネの返答を生成する"""
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
                max_output_tokens=150,
            ),
        )
        # 余分な改行や記号を除去
        reply_text = response.text.strip().replace("\n", " ")
        return reply_text
    except Exception as e:
        print(f"【LLMエラー】: {e}")
        return "ごめんね、うまく聞き取れなかったよ。もう一度教えてくれる？"


def speak_llm_reply(sock, user_text: str):
    """LLMの回答を生成し、MMDAgent-EX のソケットへ送信して喋らせる"""
    print(f"【ユーザー発話】: {user_text}")
    
    # 1. Gemini から回答を取得
    reply = generate_llm_response(user_text)
    print(f"【ジェネの回答】: {reply}")

    # 2. MMDAgent-EX へ音声合成（発話）コマンドを送信
    if sock is not None:
        try:
            command = f"SYNTH_START|0|mei_voice_normal|{reply}\n"
            sock.sendall(command.encode("utf-8"))
            print("【送信】LLMの回答を MMDAgent-EX へ送信しました。")
        except Exception as e:
            print(f"【送信エラー】: {e}")