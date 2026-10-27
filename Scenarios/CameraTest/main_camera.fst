#main_camera.fst
LOOP LOOP:
    MMD_CAMERA_GET|keyboard_0 SYNTH_START|0|mei_voice_normal|キーボードのゼロが押されました
    SYNTH_EVENT_STOP|0 <eps>

LOOP LOOP:
    MMD_CAMERA_GET|face_detect SYNTH_START|0|mei_voice_normal|顔が検出されました
    SYNTH_EVENT_STOP|0 <eps>

LOOP LOOP:
    MMD_CAMERA_GET|marker_id0 SYNTH_START|0|mei_voice_normal|マーカーのゼロ番が検出されました
    SYNTH_EVENT_STOP|0 <eps>

LOOP LOOP:
    @RECOG\_EVENT\_STOP\|.*さようなら.*@ <eps>
    +@RECOG\_EVENT\_STOP\|.*さよなら.*@ <eps>
    #
    <eps> SYNTH_START|0|mei_voice_normal|ありがとう。ばいばい！
    #
    SYNTH_EVENT_STOP|0 <eps>
