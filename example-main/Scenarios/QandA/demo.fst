${myname}=ジェネ
${chara}=Gene
${lib_dir}=../../Lib
${image_dir}=${lib_dir}/images
${motion_dir}=${lib_dir}/motions
${action_dir}=${motion_dir}/action

# 初期化（ステージ・モデル・モーション読み込み）
0 INIT1:
    <eps> STAGE|${image_dir}/floor_white.png,${image_dir}/back_lightyellow.png
    <eps> MODEL_ADD|0|${lib_dir}/gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|${motion_dir}/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> WINDOWFRAME|${image_dir}/frame_green.png

# カメラ位置設定後に待機ステート (WAIT) へ直行（起動時の挨拶はなし）
INIT1 WAIT:
    <eps> CAMERA|0,14.75,0|4.5,0,0|22.4|27.0

## メインシナリオ読み込み
%INCLUDE(love.fst)