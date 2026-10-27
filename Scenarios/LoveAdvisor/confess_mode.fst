# ==============================================================================
# confess_mode.fst : モード②「告白予行練習」シナリオ
# ==============================================================================

# --- モード起動（ボタン1選択 または 音声認識） ---
WAIT CONF_START:
    PROMPT_EVENT_SELECTED|1 PROMPT_EXIT
    @RECOG_EVENT_STOP\|.*告白.*@ PROMPT_EXIT
    +@RECOG_EVENT_STOP\|.*予行.*@ PROMPT_EXIT
    +@RECOG_EVENT_STOP\|.*練習.*@ PROMPT_EXIT

CONF_START CONF_WAIT_INPUT:
    <eps> TIMER_CANCEL|behavior
    <eps> TIMER_CANCEL|blink
    <eps> MOTION_ADD|0|action|${action_dir}/mei/mei_greeting.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|action SYNTH_START|0|mei_happy|私に告白して練習すればきっとうまくいく！さあはじめよ！私の目をしっかり見て「好きです」って言ってみて！

# --- 「好き」系の発話待ち ---
CONF_WAIT_INPUT CONF_WAIT_EYE:
    @RECOG_EVENT_STOP\|.*(好き|すき|付き合|つきあ|愛して).*@ <eps>

# キーワードが聞こえなかった場合のリトライ
CONF_WAIT_INPUT CONF_WAIT_INPUT:
    @RECOG_EVENT_STOP\|.*@ SYNTH_START|0|mei_normal|照れないで、「好きです」か「付き合ってください」って言ってみて！

# --- Python視線判定（Socket受信）の分岐 ---
# 【NG判定】目線が泳いでいる
CONF_WAIT_EYE CONF_END:
    SOCKET_RECV|VISION_EYE_NG <eps>
    <eps> MOTION_ADD|0|action|${gene_dir}/05_gracefulsmile.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|action SYNTH_START|0|mei_normal|目線が泳いでいるよ！照れないで目をみて！

# 【OK判定】しっかり目が合っている
CONF_WAIT_EYE CONF_END:
    SOCKET_RECV|VISION_EYE_OK <eps>
    <eps> MOTION_ADD|0|action|${gene_dir}/03_smile.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|action SYNTH_START|0|mei_bashful|わぁ…！そんな目で見つめられたら、絶対OKしちゃうよ！

# --- 練習終了後、自動的にメインメニューへ復帰 ---
CONF_END WAIT:
    SYNTH_EVENT_STOP|0 PROMPT_SHOW|モードを選択してね|アプローチ相談|告白予行練習
    <eps> MOTION_DELETE|0|action
    <eps> TIMER_START|blink|6