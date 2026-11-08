#
# 一般的な質問に対する応答
#
${lib_dir}=../../Lib
${action_dir}=${lib_dir}/motions/action
${gene_dir}=${lib_dir}/gene/motion

WAIT WAIT:
    @RECOG\_EVENT\_STOP\|.*こんにち.*@ <eps>
    +@RECOG\_EVENT\_STOP\|.*こんち.*@ <eps>
    # suspend behaviors
    <eps> TIMER_CANCEL|behavior
    TIMER_EVENT_CANCELLED|behavior TIMER_START|behavior|20
    <eps> TIMER_CANCEL|blink
    # action
    <eps> MOTION_ADD|0|action|${action_dir}/mei/mei_greeting.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|action SYNTH_START|0|mei_voice_normal|こんにちは
    SYNTH_EVENT_STOP|0 <eps>
    # resume behaviors
    <eps> TIMER_START|blink|6

WAIT WAIT:
    @RECOG\_EVENT\_STOP\|.*あなた.*誰.*@ <eps>
    +@RECOG\_EVENT\_STOP\|.*自己紹介.*@ <eps>
    +@RECOG\_EVENT\_STOP\|.*君.*誰.*@ <eps>
    # suspend behaviors
    <eps> TIMER_CANCEL|behavior
    TIMER_EVENT_CANCELLED|behavior TIMER_START|behavior|20
    <eps> TIMER_CANCEL|blink
    # action
    <eps> MOTION_ADD|0|action|${action_dir}/mei/mei_self_introduction.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|action SYNTH_START|0|mei_voice_normal|僕は、${myname}っていうんだ。
    SYNTH_EVENT_STOP|0 MOTION_CHANGE|0|action|${gene_dir}/03_smile.vmd
    <eps> SYNTH_START|0|mei_voice_happy|よろしくね！
    SYNTH_EVENT_STOP|0 MOTION_DELETE|0|action
    # resume behaviors
    <eps> TIMER_START|blink|6

WAIT WAIT:
    @RECOG\_EVENT\_STOP\|.*ありがと.*@ <eps>
    # suspend behaviors
    <eps> TIMER_CANCEL|behavior
    TIMER_EVENT_CANCELLED|behavior TIMER_START|behavior|20
    <eps> TIMER_CANCEL|blink
    # action
    <eps> MOTION_ADD|0|action|${gene_dir}/03_smile.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|action SYNTH_START|0|mei_voice_happy|どういたしまして！お役に立てて嬉しいよ。
    SYNTH_EVENT_STOP|0 MOTION_DELETE|0|action
    MOTION_EVENT_DELETE|0|action <eps>
    # resume behaviors
    <eps> TIMER_START|blink|6

WAIT PRETTY_BRANCH:
    @RECOG\_EVENT\_STOP\|.*可愛い.*@ <eps>
    +@RECOG\_EVENT\_STOP\|.*綺麗.*@ <eps>
    +@RECOG\_EVENT\_STOP\|.*きれい.*@ <eps>
    # suspend behaviors
    <eps> TIMER_CANCEL|behavior
    TIMER_EVENT_CANCELLED|behavior TIMER_START|behavior|20
    <eps> TIMER_CANCEL|blink
    # action
    <eps> MOTION_ADD|0|action|${gene_dir}/05_gracefulsmile.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|action VALUE_SET|random|0|100
    <eps> VALUE_EVAL|random|LE|80

PRETTY_BRANCH PRETTY_FINISH VALUE_EVENT_EVAL|random|LE|80|TRUE SYNTH_START|0|mei_voice_bashful|恥ずかしいです。
PRETTY_BRANCH PRETTY_FINISH VALUE_EVENT_EVAL|random|LE|80|FALSE SYNTH_START|0|mei_voice_bashful|ありがとう。

PRETTY_FINISH WAIT:
    SYNTH_EVENT_STOP|0 MOTION_DELETE|0|action
    MOTION_EVENT_DELETE|0|action <eps>
    # resume behaviors
    <eps> TIMER_START|blink|6

WAIT WAIT:
    @RECOG\_EVENT\_STOP\|.*さようなら.*@ <eps>
    +@RECOG\_EVENT\_STOP\|.*さよなら.*@ <eps>
    +@RECOG\_EVENT\_STOP\|.*ばいばい.*@ <eps>
    +@RECOG\_EVENT\_STOP\|.*バイバイ.*@ <eps>
    # suspend behaviors
    <eps> TIMER_CANCEL|behavior
    TIMER_EVENT_CANCELLED|behavior TIMER_START|behavior|20
    <eps> TIMER_CANCEL|blink
    # action
    <eps> MOTION_ADD|0|action|${action_dir}/wavehand.vmd|PART|ONCE|ON|OFF
    MOTION_EVENT_ADD|0|action SYNTH_START|0|mei_voice_happy|ありがとう。ばいばい！
    SYNTH_EVENT_STOP|0 <eps>
    # resume behaviors
    <eps> TIMER_START|blink|6

WAIT WAIT:
    @RECOG\_EVENT\_STOP\|.*図書館.*@ <eps>
    # suspend behaviors
    <eps> TIMER_CANCEL|behavior
    TIMER_EVENT_CANCELLED|behavior TIMER_START|behavior|20
    <eps> TIMER_CANCEL|blink
    # action
    <eps> MODEL_ADD|panel|map_library.pmd|0.0,2.8,2.5|0.0,0.0,0.0|ON|0
    <eps> MOTION_ADD|0|action|${action_dir}/mei/mei_panel_on.vmd|PART|ONCE
    <eps> MOTION_CHANGE|0|base|${action_dir}/mei/mei_guide_normal.vmd
    <eps> SYNTH_START|0|mei_voice_normal|図書館は、正面から見ると、右前の方向にあります。
    SYNTH_EVENT_STOP|0 MOTION_ADD|0|look|${action_dir}/mei/mei_look_down.vmd|PART|ONCE
    <eps> SYNTH_START|0|mei_voice_normal|キャンパスマップでは、こちらになります。
    <eps> MOTION_ADD|0|action|${action_dir}/mei/mei_point_center_buttom.vmd|PART|ONCE
    SYNTH_EVENT_STOP|0 MOTION_CHANGE|0|base|${action_dir}/mei/mei_guide_happy.vmd
    <eps> SYNTH_START|0|mei_voice_normal|お解りになりますか？
    SYNTH_EVENT_STOP|0 MODEL_DELETE|panel
    <eps> MOTION_CHANGE|0|base|${lib_dir}/motions/wait/01_Wait_b.vmd
    # resume behaviors
    <eps> TIMER_START|blink|6

WAIT WAIT:
    @RECOG\_EVENT\_STOP\|.*スクリーン.*@ <eps>
    # suspend behaviors
    <eps> TIMER_CANCEL|behavior
    TIMER_EVENT_CANCELLED|behavior TIMER_START|behavior|20
    <eps> TIMER_CANCEL|blink
    # action
    <eps> KEY_POST|MMDAgent|F|OFF
    <eps> SYNTH_START|0|mei_voice_normal|スクリーンの設定を、変更しました。
    SYNTH_EVENT_STOP|0 <eps>
    # resume behaviors
    <eps> TIMER_START|blink|6

WAIT WAIT:
    @RECOG\_EVENT\_STOP\|.*別の人.*@ <eps>
    # suspend behaviors
    <eps> TIMER_CANCEL|behavior
    TIMER_EVENT_CANCELLED|behavior TIMER_START|behavior|20
    <eps> TIMER_CANCEL|blink
    # action
    <eps> MODEL_CHANGE|0|${lib_dir}/uka/MS_Uka.pmd
    MODEL_EVENT_CHANGE|0 WINDOWFRAME|${lib_dir}/images/frame_trad.png
    <eps> SYNTH_START|0|mei_voice_low|私はウカだ。よろしくな。
    SYNTH_EVENT_STOP|0 MODEL_CHANGE|0|${lib_dir}/gene/Gene.pmd
    <eps> WINDOWFRAME|${lib_dir}/images/frame_green.png
    # resume behaviors
    <eps> TIMER_START|blink|6

WAIT WAIT:
    @RECOG\_EVENT\_STOP\|.*英語.*@ <eps>
    # suspend behaviors
    <eps> TIMER_CANCEL|behavior
    TIMER_EVENT_CANCELLED|behavior TIMER_START|behavior|20
    <eps> TIMER_CANCEL|blink
    # action
    <eps> SYNTH_START|0|slt_voice_normal|"Hello! My name is gene. How can I help you?"
    SYNTH_EVENT_STOP|0 <eps>
    # resume behaviors
    <eps> TIMER_START|blink|6







WAIT WAIT:
    MMD_CAMERA_GET|keyboard_0 SYNTH_START|0|mei_voice_normal|キーボードのゼロが押されました
    SYNTH_EVENT_STOP|0 <eps>
