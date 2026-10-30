# ==========================================
# モード①：アプローチ相談シナリオ
# ==========================================

# --- STEP 1 ---
APP_STEP1_SPEAK APP_STEP1_WAIT:
    <eps> MOTION_ADD|0|tilt|${action_dir}/mei/mei_greeting.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|tilt SYNTH_START|0|mei_voice_normal|会話やアプローチ方法で具体的にどんなことで悩んでる？なんでも話してみて！

APP_STEP1_WAIT APP_STEP1_RECOG:
    SYNTH_EVENT_STOP|0 <eps>

# --- STEP 2 ---
APP_STEP1_RECOG APP_STEP2_SPEAK:
    @RECOG_EVENT_STOP|.*仲良くなりたい.*@ <eps>
    +KEY|a <eps>

APP_STEP2_SPEAK APP_STEP2_WAIT:
    <eps> MOTION_ADD|0|nod|${action_dir}/nod.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|nod SYNTH_START|0|mei_voice_normal|なるほど、まだあまり話したことがないんだね。じゃあ、まずは自然に会話を始める方法を考えてみよう！その人と話すきっかけになりそうなことはあるかな？

APP_STEP2_WAIT APP_STEP2_RECOG:
    SYNTH_EVENT_STOP|0 <eps>

# --- STEP 3 ---
APP_STEP2_RECOG APP_STEP3_SPEAK:
    @RECOG_EVENT_STOP|.*話したことがない.*@ <eps>
    +@RECOG_EVENT_STOP|.*クラス.*@ <eps>
    +KEY|b <eps>

APP_STEP3_SPEAK APP_STEP3_WAIT:
    <eps> SYNTH_START|0|mei_voice_normal|授業や課題のことなら、自然に話しかけられそうだね！ところで、その人とは席が近い？それとも少し離れている？

APP_STEP3_WAIT APP_STEP3_RECOG:
    SYNTH_EVENT_STOP|0 <eps>

# --- STEP 4 ---
APP_STEP3_RECOG APP_STEP4_SPEAK:
    @RECOG_EVENT_STOP|.*席が近い.*@ <eps>
    +@RECOG_EVENT_STOP|.*近い.*@ <eps>
    +KEY|c <eps>

APP_STEP4_SPEAK APP_STEP4_WAIT:
    <eps> SYNTH_START|0|mei_voice_normal|それならチャンスだね！授業の前後や課題を確認するときに、さりげなく話しかけてみよう。最初から長く話そうとしなくても大丈夫だよ。

APP_STEP4_WAIT APP_STEP4_RECOG:
    SYNTH_EVENT_STOP|0 <eps>

# --- STEP 5 ---
APP_STEP4_RECOG APP_STEP5_SPEAK:
    @RECOG_EVENT_STOP|.*課題.*@ <eps>
    +@RECOG_EVENT_STOP|.*聞ける.*@ <eps>
    +KEY|d <eps>

APP_STEP5_SPEAK APP_STEP5_WAIT:
    <eps> MOTION_ADD|0|smile|${action_dir}/mei/mei_guide_happy.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|smile SYNTH_START|0|mei_voice_normal|いいね！最初は課題について聞くだけでも十分だよ。相手が答えてくれたら『ありがとう！』って伝えよう。相手も話を続けてくれたら、そこから少しずつ会話を広げてみるといいね。話しかけるのって、ちょっと緊張するよね。じゃあ、無理のない目標を決めてみよう！

APP_STEP5_WAIT APP_STEP5_RECOG:
    SYNTH_EVENT_STOP|0 <eps>

# --- STEP 6 ---
APP_STEP5_RECOG APP_STEP6_SPEAK:
    @RECOG_EVENT_STOP|.*質問.*@ <eps>
    +KEY|e <eps>

APP_STEP6_SPEAK APP_STEP6_WAIT:
    <eps> MOTION_ADD|0|cheer|${action_dir}/mei/mei_guts.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|cheer SYNTH_START|0|mei_voice_normal|いいね！最初から仲良くなろうとしなくても大丈夫。一度話せたら、それだけでも一歩前進だよ！うまく話せなくても、また次のチャンスを考えればいいからね。

APP_STEP6_WAIT WAIT:
    SYNTH_EVENT_STOP|0 <eps>