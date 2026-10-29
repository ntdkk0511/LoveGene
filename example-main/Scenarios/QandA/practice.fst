# ==========================================
# モード②：告白予行モードシナリオ
# ==========================================

# 1. 練習開始の呼びかけ
PRACTICE_START PRAC_STEP1_SPEAK:
    <eps> SYNTH_START|0|mei_voice_normal|私に告白して練習すればきっとうまくいく！さあはじめよ！私の目をしっかり見て『好きです』って言ってみて！

PRAC_STEP1_SPEAK PRAC_STEP1_WAIT:
    SYNTH_EVENT_STOP|0 <eps>

# 2. ユーザ「好きです」に対して判定値を評価（0〜100の乱数をセット）
PRAC_STEP1_WAIT PRAC_EVAL:
    @RECOG_EVENT_STOP|.*好きです.*@ VALUE_SET|random|0|100

# 3-A. OK応答（乱数50以下）
PRAC_EVAL PRAC_OK_SPEAK:
    VALUE_EVAL|random|LE|50 SYNTH_START|0|mei_voice_normal|わぁ…！そんな目で見つめられたら、絶対OKしちゃうよ！

# 3-B. NG応答（乱数51以上）
PRAC_EVAL PRAC_NG_SPEAK:
    VALUE_EVAL|random|GT|50 SYNTH_START|0|mei_voice_normal|目線が泳いでいるよ！照れないで目をみて！

PRAC_OK_SPEAK WAIT:
    SYNTH_EVENT_STOP|0 <eps>

PRAC_NG_SPEAK WAIT:
    SYNTH_EVENT_STOP|0 <eps>