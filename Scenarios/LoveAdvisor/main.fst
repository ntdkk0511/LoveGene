${myname}=ジェネ
${chara}=Gene
${lib_dir}=../../Lib
${voice_dir}=${lib_dir}/voice
${image_dir}=${lib_dir}/images
${action_dir}=${lib_dir}/motions/action
${gene_dir}=${lib_dir}/gene/motion

0 INIT1:
    <eps> STAGE|${image_dir}/floor_white.png,${image_dir}/back_lightyellow.png
    <eps> MODEL_ADD|0|${lib_dir}/gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|${lib_dir}/motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> WINDOWFRAME|${image_dir}/frame_green.png

INIT1 GREET:
    <eps> CAMERA|0,14.75,0|4.5,0,0|22.4|27.0

GREET GREETING_WAIT:
    <eps> SYNTH_START|0|mei_normal|恋のお悩み相談だよ！「アプローチ相談」か「告白予行練習」、どっちにする？

GREETING_WAIT WAIT:
    SYNTH_EVENT_STOP|0 PROMPT_SHOW|モードを選択してね|アプローチ相談|告白予行練習

%INCLUDE(approach_mode.fst)
%INCLUDE(confess_mode.fst)