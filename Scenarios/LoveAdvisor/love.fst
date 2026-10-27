
${lib_dir}=../../Lib

# ----------------------------------------
# 通常の会話・モード選択
# ----------------------------------------

WAIT WAIT:
    @RECOG_EVENT_STOP\|.*アプローチ相談.*@ <eps>
    <eps> SYNTH_START|0|mei_voice_happy|好きな人に近づく方法を一緒に考えよう！まず、好きな人とはどんな関係かな？

WAIT WAIT:
    @RECOG_EVENT_STOP\|.*告白予行.*@ <eps>
    +@RECOG_EVENT_STOP\|.*告白の練習.*@ <eps>
    <eps> SYNTH_START|0|mei_voice_happy|私に告白して練習すればきっとうまくいくよ！さあ、はじめよう！私の目をしっかり見て、好きですって言ってみて！

WAIT WAIT:
    @RECOG_EVENT_STOP\|.*こんにちは.*@ <eps>
    +@RECOG_EVENT_STOP\|.*おはよう.*@ <eps>
    <eps> SYNTH_START|0|mei_voice_normal|こんにちは！今日はどんな相談をしたいの？

WAIT WAIT:
    @RECOG_EVENT_STOP\|.*ありがとう.*@ <eps>
    <eps> SYNTH_START|0|mei_voice_happy|どういたしまして！またいつでも相談してね！

# ----------------------------------------
# ① アプローチ相談
# ----------------------------------------

WAIT ADVICE_RELATION:
    @RECOG_EVENT_STOP\|.*アプローチ相談.*@ <eps>
    +@RECOG_EVENT_STOP\|.*一番.*@ <eps>
    <eps> SYNTH_START|0|mei_voice_happy|好きな人に近づく方法を一緒に考えよう！まず、好きな人とはどんな関係かな？

ADVICE_RELATION ADVICE_NEXT:
    @RECOG_EVENT_STOP\|.*@ <eps>
    <eps> SYNTH_START|0|mei_voice_normal|なるほど！まずは挨拶や共通の話題から、少しずつ会話を増やしてみよう。相手が話しやすい雰囲気を作ることが大切だよ！

ADVICE_NEXT WAIT:
    SYNTH_EVENT_STOP\|0 <eps>

# ----------------------------------------
# ② 告白予行モード
# ----------------------------------------

WAIT CONFESSION_WAIT:
    @RECOG_EVENT_STOP\|.*告白予行.*@ <eps>
    +@RECOG_EVENT_STOP\|.*告白の練習.*@ <eps>
    +@RECOG_EVENT_STOP\|.*二番.*@ <eps>
    <eps> SYNTH_START|0|mei_voice_happy|私に告白して練習すればきっとうまくいくよ！さあ、はじめよう！私の目をしっかり見て、好きですって言ってみて！

CONFESSION_WAIT CONFESSION_FEEDBACK:
    @RECOG_EVENT_STOP\|.*好きです.*@ <eps>
    +@RECOG_EVENT_STOP\|.*好きだよ.*@ <eps>
    <eps> SYNTH_START|0|mei_voice_bashful|わぁ、告白してくれたんだね！目を見て言えたかな？「目を見て言えた」か「目線が泳いだ」と答えてね！

# 目線OKを音声で選ぶ
CONFESSION_FEEDBACK WAIT:
    @RECOG_EVENT_STOP\|.*目を見て言えた.*@ <eps>
    +@RECOG_EVENT_STOP\|.*ちゃんと見た.*@ <eps>
    <eps> SYNTH_START|0|mei_voice_happy|OK！わぁ、そんな目で見つめられたら、絶対OKしちゃうよ！

# 目線NGを音声で選ぶ
CONFESSION_FEEDBACK WAIT:
    @RECOG_EVENT_STOP\|.*目線が泳いだ.*@ <eps>
    +@RECOG_EVENT_STOP\|.*緊張した.*@ <eps>
    <eps> SYNTH_START|0|mei_voice_normal|NG！少し目線が泳いでいたみたい。照れずに相手の目を見て、もう一度ゆっくり伝えてみよう！

# ----------------------------------------
# 告白予行中の再挑戦
# ----------------------------------------

WAIT CONFESSION_WAIT:
    @RECOG_EVENT_STOP\|.*もう一回.*@ <eps>
    +@RECOG_EVENT_STOP\|.*もう一度.*@ <eps>
    <eps> SYNTH_START|0|mei_voice_happy|もちろん！私の目をしっかり見て、好きですって言ってみて！
