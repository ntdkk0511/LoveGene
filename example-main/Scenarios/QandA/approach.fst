# ==========================================
# モード①：アプローチ相談シナリオ
# ==========================================

# 1. Gene「会話やアプローチ方法で具体的にどんなことで悩んでる？なんでも話してみて！」
APPROACH_START APP_STEP1_SPEAK:
    <eps> MOTION_ADD|0|tilt|${action_dir}/mei/mei_head_tilt.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|tilt SYNTH_START|0|mei_voice_normal|会話やアプローチ方法で具体的にどんなことで悩んでる？なんでも話してみて！

APP_STEP1_SPEAK APP_STEP1_WAIT:
    SYNTH_EVENT_STOP|0 <eps>

# 2. ユーザ「好きな人と仲良くなりたい」 -> Gene「なるほど、まだあまり〜」
APP_STEP1_WAIT APP_STEP2_SPEAK:
    @RECOG_EVENT_STOP|.*仲良くなりたい.*@ MOTION_ADD|0|nod|${action_dir}/mei/mei_nod.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|nod SYNTH_START|0|mei_voice_normal|なるほど、まだあまり話したことがないんだね。じゃあ、まずは自然に会話を始める方法を考えてみよう！その人と話すきっかけになりそうなことはあるかな？

APP_STEP2_SPEAK APP_STEP2_WAIT:
    SYNTH_EVENT_STOP|0 <eps>

# 3. ユーザ「同じクラスだけど、ほとんど話したことがない」 -> Gene「授業や課題のことなら〜」
APP_STEP2_WAIT APP_STEP3_SPEAK:
    @RECOG_EVENT_STOP|.*話したことがない.*@ SYNTH_START|0|mei_voice_normal|授業や課題のことなら、自然に話しかけられそうだね！ところで、その人とは席が近い？それとも少し離れている？
    +@RECOG_EVENT_STOP|.*クラス.*@ SYNTH_START|0|mei_voice_normal|授業や課題のことなら、自然に話しかけられそうだね！ところで、その人とは席が近い？それとも少し離れている？

APP_STEP3_SPEAK APP_STEP3_WAIT:
    SYNTH_EVENT_STOP|0 <eps>

# 4. ユーザ「席が近い」 -> Gene「それならチャンスだね！〜」
APP_STEP3_WAIT APP_STEP4_SPEAK:
    @RECOG_EVENT_STOP|.*席が近い.*@ SYNTH_START|0|mei_voice_normal|それならチャンスだね！授業の前後や課題を確認するときに、さりげなく話しかけてみよう。最初から長く話そうとしなくても大丈夫だよ。
    +@RECOG_EVENT_STOP|.*近い.*@ SYNTH_START|0|mei_voice_normal|それならチャンスだね！授業の前後や課題を確認するときに、さりげなく話しかけてみよう。最初から長く話そうとしなくても大丈夫だよ。

APP_STEP4_SPEAK APP_STEP4_WAIT:
    SYNTH_EVENT_STOP|0 <eps>

# 5. ユーザ「課題についてなら聞けるかも」 -> Gene「いいね！〜」
APP_STEP4_WAIT APP_STEP5_SPEAK:
    @RECOG_EVENT_STOP|.*課題.*@ MOTION_ADD|0|smile|${action_dir}/mei/mei_smile.vmd|PART|ONCE|ON|OFF
    +@RECOG_EVENT_STOP|.*聞ける.*@ MOTION_ADD|0|smile|${action_dir}/mei/mei_smile.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|smile SYNTH_START|0|mei_voice_normal|いいね！最初は課題について聞くだけでも十分だよ。相手が答えてくれたら『ありがとう！』って伝えよう。相手も話を続けてくれたら、そこから少しずつ会話を広げてみるといいね。話しかけるのって、ちょっと緊張するよね。じゃあ、無理のない目標を決めてみよう！

APP_STEP5_SPEAK APP_STEP5_WAIT:
    SYNTH_EVENT_STOP|0 <eps>

# 6. ユーザ「授業や課題について質問する。」 -> Gene「いいね！最初から〜」
APP_STEP5_WAIT APP_STEP6_SPEAK:
    @RECOG_EVENT_STOP|.*質問.*@ MOTION_ADD|0|cheer|${action_dir}/mei/mei_cheer.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|cheer SYNTH_START|0|mei_voice_normal|いいね！最初から仲良くなろうとしなくても大丈夫。一度話せたら、それだけでも一歩前進だよ！うまく話せなくても、また次のチャンスを考えればいいからね。

APP_STEP6_SPEAK WAIT:
    SYNTH_EVENT_STOP|0 <eps>