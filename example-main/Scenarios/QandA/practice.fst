# ==========================================
# モード②：告白予行モード
# ==========================================

PRACTICE_START PRAC_STEP1_SPEAK:
    <eps> SYNTH_START|0|mei_voice_normal|私に告白して練習すればきっとうまくいく！さあはじめよ！私の目をしっかり見て『好きです』って言ってみて！

PRAC_STEP1_SPEAK PRAC_STEP1_RECOG:
    SYNTH_EVENT_STOP|0 <eps>

# 「好きです」の認識（キー [o] で OK 判定テスト、キー [n] で NG 判定テスト）
PRAC_STEP1_RECOG PRAC_OK_SPEAK:
    @RECOG_EVENT_STOP|.*好きです.*@ <eps>
    +KEY|o <eps>

PRAC_STEP1_RECOG PRAC_NG_SPEAK:
    KEY|n <eps>

# --- 判定結果：OK ---
PRAC_OK_SPEAK WAIT:
    <eps> MOTION_ADD|0|smile|${action_dir}/mei/mei_guide_happy.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|smile SYNTH_START|0|mei_voice_normal|わぁ…！そんな目で見つめられたら、絶対OKしちゃうよ！

# --- 判定結果：NG ---
PRAC_NG_SPEAK WAIT:
    <eps> SYNTH_START|0|mei_voice_normal|目線が泳いでいるよ！照れないで目をみて！