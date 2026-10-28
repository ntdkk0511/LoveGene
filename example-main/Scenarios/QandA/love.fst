#
# 恋愛相談への応答
#

WAIT WAIT:
    @RECOG\_EVENT\_STOP\|.*恋愛相談.*@ <eps>
    # 待機動作の調整
    <eps> TIMER_CANCEL|behavior
    TIMER_EVENT_CANCELLED|behavior TIMER_START|behavior|20
    <eps> TIMER_CANCEL|blink
    # 発話
    <eps> SYNTH_START|0|mei_voice_normal|どんな相談があるの？
    SYNTH_EVENT_STOP|0 <eps>
    # 瞬きの再開
    <eps> TIMER_START|blink|6