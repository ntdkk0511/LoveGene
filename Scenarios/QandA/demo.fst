${myname}=ジェネ
${chara}=Gene
${lib_dir}=../../Lib
${image_dir}=${lib_dir}/images

0 INIT1:
    <eps> STAGE|${image_dir}/floor_white.png,${image_dir}/back_lightyellow.png
    <eps> MODEL_ADD|0|${lib_dir}/gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|${lib_dir}/motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> WINDOWFRAME|${image_dir}/frame_green.png
#    <eps> MODEL_BINDFACE|0|メッシュなし|1
#    <eps> MODEL_BINDFACE|0|髪留なし|1
#    <eps> MODEL_BINDFACE|0|頬なし|1

# カメラ設定: INIT1 -> WAIT

INIT1 WAIT:
    <eps> CAMERA|0,14.75,0|4.5,0,0|22.4|27.0

## メインループ WAIT to WAIT

%INCLUDE(demo_qa.fst)
%INCLUDE(love.fst)


