#
# Sample script for Quiz
#                     by Motoyuki Suzuki
#
${lib_dir}=../../Lib
${action_dir}=${lib_dir}/motions/action
${gene_dir}=${lib_dir}/gene/motion

WAIT WAIT:
    @RECOG\_EVENT\_STOP\|.*こんにち.*@ <eps>
    +@RECOG\_EVENT\_STOP\|.*こんち.*@ <eps>
    <eps> MOTION_ADD|0|action|${action_dir}/mei/mei_greeting.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|action SYNTH_START|0|mei_voice_normal|こんにちは
    SYNTH_EVENT_STOP|0 <eps>
#
# Quiz
#
WAIT ASK_NAME:
    @RECOG\_EVENT\_STOP\|.*クイズ.*@  SYNTH_START|0|mei_voice_normal|クイズをしましょう
    SYNTH_EVENT_STOP|0  <eps>

ASK_NAME NAME_CONFIRM:
    <eps>  SYNTH_START|0|mei_voice_normal|お名前を教えてください
    SYNTH_EVENT_STOP|0  <eps>
    @RECOG\_EVENT\_STOP\|(.*名前は)?(.*)(です|でーす|といいます).*@  <eps>  ${name}=${2}

NAME_CONFIRM ASK_NAME:
    ${name}=="" SYNTH_START|0|mei_voice_normal|すみません，聞きとれませんでした。
    SYNTH_EVENT_STOP|0  <eps>

NAME_CONFIRM Q1:
     ${name}!=""  SYNTH_START|0|mei_voice_normal|${name}さんですね。
     SYNTH_EVENT_STOP|0  SYNTH_START|0|mei_voice_normal|それでは，クイズを始めましょう。
     SYNTH_EVENT_STOP|0  VALUE_SET|noCorr|0
#
# 第1問
#
Q1 WAIT_ANS1:
   <eps>  SYNTH_START|0|mei_voice_normal|第1問。
   SYNTH_EVENT_STOP|0  SYNTH_START|0|mei_voice_normal|花札に使われる植物。1月は松，2月は梅。では，3月は何でしょう？
   <eps>  PROMPT_SHOW|マウスでクリックしてね|竹|藤|桜

WAIT_ANS1 YESNO1:
    PROMPT_EVENT_SELECTED|0  <eps> ${ans}="たけ"
    +PROMPT_EVENT_SELECTED|1  <eps> ${ans}="ふじ"
    +PROMPT_EVENT_SELECTED|2  <eps> ${ans}="さくら"
   <eps>  SYNTH_START|0|mei_voice_normal|${ans}でいいですか？
   SYNTH_EVENT_STOP|0  <eps>

YESNO1 ANS_CHECK1:
   @RECOG\_EVENT\_STOP\|.*(はい|そう|うん|いいです).*@ <eps>

YESNO1 Q1:
   @RECOG\_EVENT\_STOP\|.*(いいえ|違う|違います|だめ).*@ SYNTH_START|0|mei_voice_normal|では，もう一度。
   SYNTH_EVENT_STOP|0  <eps>   

ANS_CHECK1 Q2:
   ${ans}=="さくら"  SYNTH_START|0|mei_voice_normal|正解です。${name}さん，素晴しいです。
   SYNTH_EVENT_STOP|0  VALUE_SET|noCorr|1

ANS_CHECK1 Q2:
   ${ans}!="さくら"  SYNTH_START|0|mei_voice_normal|残念，不正解です。${name}さん，常識ないですね。
   SYNTH_EVENT_STOP|0  <eps>   

#
# 第2問
#
Q2 WAIT_ANS2:
   <eps>  SYNTH_START|0|mei_voice_normal|続いて，第2問。
   SYNTH_EVENT_STOP|0  SYNTH_START|0|mei_voice_normal|初夢で見ると縁起がよいと言われるもの。いち富士，に鷹。三は何でしょう？
   <eps>  PROMPT_SHOW|マウスでクリックしてね|松|宝船|茄子

WAIT_ANS2 YESNO2:
    PROMPT_EVENT_SELECTED|0 <eps> ${ans}="松"
    +PROMPT_EVENT_SELECTED|1 <eps> ${ans}="宝船"
    +PROMPT_EVENT_SELECTED|2 <eps> ${ans}="茄子"
    <eps>  SYNTH_START|0|mei_voice_normal|${ans}でいいですか？
    SYNTH_EVENT_STOP|0  <eps>

YESNO2 ANS_CHECK2:
    @RECOG\_EVENT\_STOP\|.*(はい|そう|うん|いいです).*@ <eps>

YESNO2 Q2:
    @RECOG\_EVENT\_STOP\|.*(いいえ|違う|違います|だめ).*@ SYNTH_START|0|mei_voice_normal|では，もう一度。
    SYNTH_EVENT_STOP|0  <eps>   

ANS_CHECK2 Q3:
    ${ans}=="茄子"  SYNTH_START|0|mei_voice_normal|正解です。${name}さん，素晴しいです。
    SYNTH_EVENT_STOP|0  VALUE_EVAL|noCorr|EQ|1
    VALUE_EVENT_EVAL|noCorr|EQ|1|TRUE  VALUE_SET|noCorr|2
    +VALUE_EVENT_EVAL|noCorr|EQ|1|FALSE  VALUE_SET|noCorr|1

ANS_CHECK2 Q3:
   ${ans}!="茄子"  SYNTH_START|0|mei_voice_normal|残念，不正解です。${name}さん，常識ないですね。
   SYNTH_EVENT_STOP|0  <eps>   

#
# 第3問
#
Q3 WAIT_ANS3:
   <eps>  SYNTH_START|0|mei_voice_normal|最後，第3問。
   SYNTH_EVENT_STOP|0  SYNTH_START|0|mei_voice_normal|次の神様の中で，七福神に含まれないのは，誰でしょう？
   <eps>  PROMPT_SHOW|マウスでクリックしてね|恵比須|寿老人|吉祥天|福禄寿

WAIT_ANS3 YESNO3:
    PROMPT_EVENT_SELECTED|0  <eps>  ${ans}="恵比須"
    +PROMPT_EVENT_SELECTED|1  <eps>  ${ans}="寿老人"
    +PROMPT_EVENT_SELECTED|2  <eps>  ${ans}="きっしょうてん"
    +PROMPT_EVENT_SELECTED|3  <eps>  ${ans}="ふくろくじゅ"
    <eps>  SYNTH_START|0|mei_voice_normal|${ans}でいいですか？
    SYNTH_EVENT_STOP|0  <eps>

YESNO3 ANS_CHECK3:
   @RECOG\_EVENT\_STOP\|.*(はい|そう|うん|いいです).*@ <eps>

YESNO3 Q3:
   @RECOG\_EVENT\_STOP\|.*(いいえ|違う|違います|だめ).*@ SYNTH_START|0|mei_voice_normal|では，もう一度。
   SYNTH_EVENT_STOP|0  <eps>   

ANS_CHECK3 ADD_SCORE3:
   ${ans}=="きっしょうてん"  SYNTH_START|0|mei_voice_normal|正解です。${name}さん，素晴しいです。
   SYNTH_EVENT_STOP|0  VALUE_EVAL|noCorr|EQ|2

ADD_SCORE3 ENDING VALUE_EVENT_EVAL|noCorr|EQ|2|TRUE  VALUE_SET|noCorr|3
ADD_SCORE3 ENDING:
    VALUE_EVENT_EVAL|noCorr|EQ|2|FALSE  VALUE_EVAL|noCorr|EQ|1
    VALUE_EVENT_EVAL|noCorr|EQ|1|TRUE  VALUE_SET|noCorr|2
    +VALUE_EVENT_EVAL|noCorr|EQ|1|FALSE  VALUE_SET|noCorr|1

ANS_CHECK3 ENDING:
   ${ans}!="きっしょうてん"  SYNTH_START|0|mei_voice_normal|残念，不正解です。${name}さん，常識ないですね。
   SYNTH_EVENT_STOP|0  <eps>   

#
# 結果発表
#
ENDING SCORE_0:
    <eps>  SYNTH_START|0|mei_voice_normal|それでは，結果発表です。
    SYNTH_EVENT_STOP|0  VALUE_EVAL|noCorr|EQ|0

SCORE_0 BYE VALUE_EVENT_EVAL|noCorr|EQ|0|TRUE  SYNTH_START|0|mei_voice_sad|${name}さんの結果は，0点でした。常識ないんですね。
SCORE_0 SCORE_1 VALUE_EVENT_EVAL|noCorr|EQ|0|FALSE  VALUE_EVAL|noCorr|EQ|1
SCORE_1 BYE  VALUE_EVENT_EVAL|noCorr|EQ|1|TRUE  SYNTH_START|0|mei_voice_sad|${name}さんの結果は，1点でした。もう少しがんばりましょう
SCORE_1 BYE:
    VALUE_EVENT_EVAL|noCorr|EQ|1|FALSE  VALUE_EVAL|noCorr|EQ|2
    VALUE_EVENT_EVAL|noCorr|EQ|2|TRUE  SYNTH_START|0|mei_voice_normal|${name}さんの結果は，2点でした。惜しかったですね。
    +VALUE_EVENT_EVAL|noCorr|EQ|2|FALSE  SYNTH_START|0|mei_voice_happy|${name}さんの結果は，満点でした。素晴しいです。

BYE WAIT:
    SYNTH_EVENT_STOP|0  SYNTH_START|0|mei_voice_normal|次回もまた挑戦してくださいね。
    SYNTH_EVENT_STOP|0  SYNTH_START|0|mei_voice_normal|それでは，さようなら。
    <eps>  MOTION_ADD|0|action|${action_dir}/mei/mei_bye.vmd|PART|ONCE
    SYNTH_EVENT_STOP|0 <eps>
