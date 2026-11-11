# ==========================================
# モード②：告白予行モード（計測・評価機能付き）
# ==========================================

# ------------------------------------------
# シナリオ開始
# ------------------------------------------
PRACTICE_START PRAC_STEP1_SPEAK:
    <eps> CAPTION_START|gene_text|gene_style|私に告白して練習すれば、きっとうまくいく！\nさあ、はじめよう！\n私の目をしっかり見て\n『好きです』って言ってみて！|1.0|CENTER|0.22|18000
    <eps> MOTION_ADD|0|app_welcome|${action_dir}/歓迎する1.vmd|PART|ONCE|ON|OFF
    <eps> SYNTH_START|0|mei_voice_normal|私に告白して練習すればきっとうまくいく！さあはじめよ！私の目をしっかり見て『好きです』って言ってみて！

# セリフが言い終わったら音声認識待ちへ
PRAC_STEP1_SPEAK PRAC_RECOG_LISTEN:
    SYNTH_EVENT_STOP|0 <eps>

# ------------------------------------------
# ユーザーの告白認識
# ------------------------------------------

# 「好き」「すき」「スキ」が含まれる音声認識（OK判定）
PRAC_RECOG_LISTEN PRAC_OK_SPEAK:
    @RECOG_EVENT_STOP|.*好き.*@ <eps>
    +@RECOG_EVENT_STOP|.*すき.*@ <eps>
    +@RECOG_EVENT_STOP|.*スキ.*@ <eps>
    +KEY|o <eps>
    +KEY|O <eps>

# NG判定（キー操作等）
PRAC_RECOG_LISTEN PRAC_NG_SPEAK:
    KEY|n <eps>
    +KEY|N <eps>

# --- 判定結果：OK ---
PRAC_OK_SPEAK PRAC_FINISHED:
    <eps> CAPTION_START|gene_text|gene_style|わぁ…！そんな目で見つめられたら、\n絶対OKしちゃうよ！|1.0|CENTER|0.22|18000
    <eps> MOTION_ADD|0|smile|${action_dir}/肯定する1.vmd|PART|ONCE|ON|OFF
    <eps> SYNTH_START|0|mei_voice_normal|わぁ…！そんな目で見つめられたら、絶対OKしちゃうよ！

# --- 判定結果：NG ---
PRAC_NG_SPEAK PRAC_FINISHED:
    <eps> CAPTION_START|gene_text|gene_style|目線が泳いでいるよ！\n照れないで目をみて！|1.0|CENTER|0.22|18000
    <eps> MOTION_ADD|0|smile|${action_dir}/喜ぶ1.vmd|PART|ONCE|ON|OFF
    <eps> SYNTH_START|0|mei_voice_normal|目線が泳いでいるよ！照れないで目をみて！

# 応答完了後、評価フローへ移行
PRAC_FINISHED N:
    SYNTH_EVENT_STOP|0 <eps>

# ------------------------------------------
# 終了・評価フロー
# ------------------------------------------

# 【テスト用】キー1で直接認識待ちへ、キー2で評価へ移行
WAIT PRAC_RECOG_LISTEN:
    KEY|1 <eps>

WAIT N:
    KEY|6 <eps>

N NE:
    <eps> CAPTION_START|gene_text|gene_style|おつかれさま|1.0|CENTER|0.22|18000
    <eps> SYNTH_START|0|mei_voice_normal|おつかれさま

NE NEX:
    SYNTH_EVENT_STOP|0 <eps>

NEX NEXT:
    <eps> CAPTION_START|gene_text|gene_style|それじゃあ評価をしていくね|1.0|CENTER|0.22|18000
    <eps> SYNTH_START|0|mei_voice_normal|それじゃあ評価をしていくね

NEXT NEXT1:
    SYNTH_EVENT_STOP|0 <eps>

# --- 表情評価・画像表示 ---
NEXT1 NEXT2:
    <eps> SYNTH_START|0|mei_voice_normal|表情の評価
    <eps> CAPTION_START|gene_text|gene_style|表情の評価|1.0|CENTER|0.22|18000
    <eps> WINDOWFRAME_ADD|result_h|result_h.png

NEXT2 NEXT21:
    MMD_CAMERA_GET|verygood_h CAPTION_START|gene_text|gene_style|よくできたね|1.0|CENTER|0.22|18000

NEXT21 NEXT3:
    <eps> SYNTH_START|0|mei_voice_happy|よくできたね！

NEXT2 NEXT22:
    MMD_CAMERA_GET|good_h CAPTION_START|gene_text|gene_style|いいね|1.0|CENTER|0.22|18000

NEXT22 NEXT3:
    <eps> SYNTH_START|0|mei_voice_normal|いいね！

NEXT2 NEXT23:
    MMD_CAMERA_GET|bad_h CAPTION_START|gene_text|gene_style|もう少し頑張ってみよう|1.0|CENTER|0.22|18000 

NEXT23 NEXT3:
    <eps> SYNTH_START|0|mei_voice_normal|もう少し頑張ってみよう！

# 表情画像削除
NEXT3 NEXT4:
    SYNTH_EVENT_STOP|0 <eps> 
    <eps> WINDOWFRAME_DELETE|result_h

# --- 視線評価・画像表示 ---
NEXT4 NEXT5:
    <eps> SYNTH_START|0|mei_voice_normal|視線の評価
    <eps> CAPTION_START|gene_text|gene_style|視線の評価|1.0|CENTER|0.22|18000
    <eps> WINDOWFRAME_ADD|result_s|result_s.png

NEXT5 NEXT71:
    MMD_CAMERA_GET|verygood_s CAPTION_START|gene_text|gene_style|よくできたね|1.0|CENTER|0.22|18000

NEXT71 NEXT7:
    <eps> SYNTH_START|0|mei_voice_happy|よくできたね

NEXT5 NEXT72:
    MMD_CAMERA_GET|good_s CAPTION_START|gene_text|gene_style|いいね|1.0|CENTER|0.22|18000

NEXT72 NEXT7:
    <eps> SYNTH_START|0|mei_voice_normal|いいね

NEXT5 NEXT73:
    MMD_CAMERA_GET|bad_s CAPTION_START|gene_text|gene_style|もう少し頑張ってみよう|1.0|CENTER|0.22|18000

NEXT73 NEXT7:
    <eps> SYNTH_START|0|mei_voice_normal|もう少し頑張ってみよう

# 視線画像削除して待機状態へ
NEXT7 WAIT:
    SYNTH_EVENT_STOP|0 WINDOWFRAME_DELETE|result_s