
# ==========================================
# モード①：アプローチ相談シナリオ
# ==========================================

# --- STEP 1：歓迎する ---
APP_STEP1_SPEAK APP_STEP1_WAIT:
    <eps> CAPTION_START|gene_text|gene_style|会話やアプローチ方法で具体的に\nどんなことで悩んでる？\nなんでも話してみて！|1.0|CENTER|0.22|18000
    <eps> MOTION_ADD|0|app_welcome|${action_dir}/歓迎する1.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|app_welcome SYNTH_START|0|mei_voice_normal|会話やアプローチ方法で具体的にどんなことで悩んでる？なんでも話してみて！

APP_STEP1_WAIT APP_STEP1_RECOG:
    SYNTH_EVENT_STOP|0 <eps>

# --- STEP 2：うなずく ---
APP_STEP1_RECOG APP_STEP2_SPEAK:
    @RECOG_EVENT_STOP|.*仲良くなりたい.*@ <eps>
    +KEY|a <eps>

APP_STEP2_SPEAK APP_STEP2_WAIT:
    <eps> CAPTION_START|gene_text|gene_style|なるほど、まだあまり話したことがないんだね。\nじゃあ、まずは自然に会話を始める方法を\n考えてみよう！\nその人と話すきっかけになりそうなことはあるかな？|1.0|CENTER|0.22|18000
    <eps> MOTION_ADD|0|app_nod|${action_dir}/tere.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|app_nod SYNTH_START|0|mei_voice_normal|なるほど、まだあまり話したことがないんだね。じゃあ、まずは自然に会話を始める方法を考えてみよう！その人と話すきっかけになりそうなことはあるかな？

APP_STEP2_WAIT APP_STEP2_RECOG:
    SYNTH_EVENT_STOP|0 <eps>

# --- STEP 3：考える ---
APP_STEP2_RECOG APP_STEP3_SPEAK:
    @RECOG_EVENT_STOP|.*話したことがない.*@ <eps>
    +@RECOG_EVENT_STOP|.*クラス.*@ <eps>
    +KEY|b <eps>

APP_STEP3_SPEAK APP_STEP3_WAIT:
    <eps> CAPTION_START|gene_text|gene_style|授業や課題のことなら、\n自然に話しかけられそうだね！\nその人とは席が近い？\nそれとも少し離れている？|1.0|CENTER|0.22|18000
    <eps> MOTION_ADD|0|app_think|${action_dir}/考える1.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|app_think SYNTH_START|0|mei_voice_normal|授業や課題のことなら、自然に話しかけられそうだね！ところで、その人とは席が近い？それとも少し離れている？

APP_STEP3_WAIT APP_STEP3_RECOG:
    SYNTH_EVENT_STOP|0 <eps>

# --- STEP 4：説明する ---
APP_STEP3_RECOG APP_STEP4_SPEAK:
    @RECOG_EVENT_STOP|.*席が近い.*@ <eps>
    +@RECOG_EVENT_STOP|.*近い.*@ <eps>
    +KEY|c <eps>

APP_STEP4_SPEAK APP_STEP4_WAIT:
    <eps> CAPTION_START|gene_text|gene_style|それならチャンスだね！\n授業の前後や課題を確認するときに、\nさりげなく話しかけてみよう。\n最初から長く話さなくても大丈夫だよ。|1.0|CENTER|0.22|18000
    <eps> MOTION_ADD|0|app_explain|${action_dir}/肯定する2.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|app_explain SYNTH_START|0|mei_voice_normal|それならチャンスだね！授業の前後や課題を確認するときに、さりげなく話しかけてみよう。最初から長く話そうとしなくても大丈夫だよ。

APP_STEP4_WAIT APP_STEP4_RECOG:
    SYNTH_EVENT_STOP|0 <eps>

# --- STEP 5：喜ぶ ---
APP_STEP4_RECOG APP_STEP5_SPEAK:
    @RECOG_EVENT_STOP|.*課題.*@ <eps>
    +@RECOG_EVENT_STOP|.*聞ける.*@ <eps>
    +KEY|d <eps>

APP_STEP5_SPEAK APP_STEP5_WAIT:
    <eps> CAPTION_START|gene_text|gene_style|いいね！最初は課題について聞くだけでも十分だよ。\n相手が答えてくれたら『ありがとう！』って伝えよう。\nそこから少しずつ会話を広げてみるといいね。\n緊張すると思うけど、無理のない目標を決めよう！|1.0|CENTER|0.22|18000
    <eps> MOTION_ADD|0|app_happy|${action_dir}/喜ぶ1.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|app_happy SYNTH_START|0|mei_voice_normal|いいね！最初は課題について聞くだけでも十分だよ。相手が答えてくれたら『ありがとう！』って伝えよう。相手も話を続けてくれたら、そこから少しずつ会話を広げてみるといいね。話しかけるのって、ちょっと緊張するよね。じゃあ、無理のない目標を決めてみよう！

APP_STEP5_WAIT APP_STEP5_RECOG:
    SYNTH_EVENT_STOP|0 <eps>

# --- STEP 6：応援する ---
APP_STEP5_RECOG APP_STEP6_SPEAK:
    @RECOG_EVENT_STOP|.*質問.*@ <eps>
    +KEY|e <eps>

APP_STEP6_SPEAK APP_STEP6_WAIT:
    <eps> CAPTION_START|gene_text|gene_style|いいね！最初から仲良くならなくても大丈夫。\n一度話せたら、それだけでも一歩前進だよ！\nうまく話せなくても、\nまた次のチャンスを考えればいいからね。|1.0|CENTER|0.22|18000
    <eps> MOTION_ADD|0|app_cheer|${action_dir}/レッツゴー.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|app_cheer SYNTH_START|0|mei_voice_normal|いいね！最初から仲良くなろうとしなくても大丈夫。一度話せたら、それだけでも一歩前進だよ！うまく話せなくても、また次のチャンスを考えればいいからね。

APP_STEP6_WAIT WAIT:
    SYNTH_EVENT_STOP|0 <eps>
