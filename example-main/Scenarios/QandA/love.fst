# --------------------------------------------------
# 初期挨拶（顔認識イベント待ちに変更）
# --------------------------------------------------
START GREET_SPEAK:
    MMD_CAMERA_GET|FACE SYNTH_START|0|mei_voice_normal|私は恋愛マスタージェネだよ！アプローチ相談も告白練習も力になるよ！

GREET_SPEAK WAIT:
    SYNTH_EVENT_STOP|0 <eps>

# --- モード選択分岐 ---
# モード①：アプローチ相談へ移動（音声「アプローチ」またはキー[1]）
WAIT APPROACH_START:
    @RECOG_EVENT_STOP|.*アプローチ.*@ <eps>
    +KEY|1 <eps>

# モード②：告白予行練習へ移動（音声「告白」「練習」またはキー[2]）
WAIT PRACTICE_START:
    @RECOG_EVENT_STOP|.*告白.*@ <eps>
    +@RECOG_EVENT_STOP|.*練習.*@ <eps>
    +KEY|2 <eps>

# --- シナリオファイルの読み込み ---
%INCLUDE(love.fst)
%INCLUDE(approach.fst)
%INCLUDE(practice.fst)