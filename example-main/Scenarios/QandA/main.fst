# 起動時の挨拶
START GREET_SPEAK:
    <eps> MMDAGENT_EVENT_START SYNTH_START|0|mei_voice_normal|私は恋愛マスタージェネだよ！アプローチ相談も告白練習も力になるよ！

GREET_SPEAK WAIT:
    SYNTH_EVENT_STOP|0 <eps>

# キーボードでテスト
WAIT WAIT:
    KEY|1 SYNTH_START|0|mei_voice_normal|こんにちは！

# アプローチ相談モード
WAIT PRACTICE_SPEAK:
    MODE_PRACTICE MOTION_ADD|0|practice|happy2.vmd|FULL|ONCE|ON|OFF

PRACTICE_SPEAK WAIT:
    <eps> SYNTH_START|0|mei_voice_normal|告白の練習を始めるよ。

WAIT CONSULT_SPEAK:
    MODE_CONSULT MOTION_ADD|0|consult|happy2.vmd|FULL|ONCE|ON|OFF

CONSULT_SPEAK WAIT:
    <eps> SYNTH_START|0|mei_voice_normal|どんなことで悩んでいるの？




