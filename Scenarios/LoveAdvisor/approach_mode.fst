# ==============================================================================
# approach_mode.fst : モード①「アプローチ相談」シナリオ
# ==============================================================================

# --- モード起動（ボタン0選択 または 音声認識） ---
WAIT APP_START:
    PROMPT_EVENT_SELECTED|0 PROMPT_EXIT
    @RECOG_EVENT_STOP\|.*アプローチ.*@ PROMPT_EXIT
    +@RECOG_EVENT_STOP\|.*相談.*@ PROMPT_EXIT

APP_START APP_MENU:
    <eps> TIMER_CANCEL|behavior
    <eps> TIMER_CANCEL|blink
    <eps> SYNTH_START|0|mei_normal|アプローチの相談だね！「ライン」「デート」「会話」のどれについてアドバイスがほしい？

APP_MENU APP_WAIT_CHOICE:
    SYNTH_EVENT_STOP|0 <eps>

# --- 話題分岐1: LINEについて ---
APP_WAIT_CHOICE APP_END:
    @RECOG_EVENT_STOP\|.*(ライン|LINE|メッセージ|メール).*@ <eps>
    <eps> MOTION_ADD|0|action|${gene_dir}/03_smile.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|action SYNTH_START|0|mei_happy|LINEは相手の返信ペースに合わせるのが基本だよ！焦らず短文で返しやすくしてみてね！

# --- 話題分岐2: デートの誘い方 ---
APP_WAIT_CHOICE APP_END:
    @RECOG_EVENT_STOP\|.*(デート|誘|ご飯|食事).*@ <eps>
    <eps> MOTION_ADD|0|action|${gene_dir}/03_smile.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|action SYNTH_START|0|mei_happy|「美味しそうなお店見つけたんだけど一緒に行かない？」って、自然な口実を作って誘うのがおすすめだよ！

# --- 話題分岐3: 最初の会話・話題 ---
APP_WAIT_CHOICE APP_END:
    @RECOG_EVENT_STOP\|.*(会話|話題|話し|きっかけ|挨拶).*@ <eps>
    <eps> MOTION_ADD|0|action|${action_dir}/mei/mei_greeting.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|action SYNTH_START|0|mei_normal|相手の趣味や最近ハマっていることを質問してみて！聞き役に回ると好印象だよ！

# --- 認識できなかった場合のリトライ ---
APP_WAIT_CHOICE APP_MENU:
    @RECOG_EVENT_STOP\|.*@ SYNTH_START|0|mei_normal|よく聞こえなかったよ。「ライン」「デート」「会話」のどれかについて聞いてみてね！

# --- 相談終了後、自動的にメインメニューへ復帰 ---
APP_END WAIT:
    SYNTH_EVENT_STOP|0 PROMPT_SHOW|モードを選択してね|アプローチ相談|告白予行練習
    <eps> MOTION_DELETE|0|action
    <eps> TIMER_START|blink|6