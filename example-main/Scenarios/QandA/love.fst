# --------------------------------------------------
# メイン待機 ＆ モード選択（ボタン / キー / 音声）
# --------------------------------------------------

# --- モード①：アプローチ相談 ---
WAIT APP_STEP1_SPEAK:
    MODE_CONSULT <eps>
    +KEY|1 <eps>
    +@RECOG_EVENT_STOP|.*アプローチ.*@ <eps>
    +@RECOG_EVENT_STOP|.*相談.*@ <eps>

# --- モード②：告白予行モード ---
WAIT PRACTICE_START:
    MODE_PRACTICE <eps>
    +KEY|2 <eps>
    +@RECOG_EVENT_STOP|.*告白.*@ <eps>
    +@RECOG_EVENT_STOP|.*練習.*@ <eps>

# 各シナリオファイルの読み込み
%INCLUDE(approach.fst)
%INCLUDE(practice.fst)