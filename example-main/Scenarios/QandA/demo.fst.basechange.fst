#
# ベースモーションを一定時間ごとに入れ替えるサブFST
#
${base_duration}=16
${basemotionid}=0
${motion_dir}=../../Lib/motions/wait

0 LOOP:
   <eps> TIMER_START|basechange|${base_duration}

# 一定時間が過ぎたらベースモーションを変える
LOOP BMCHANGE:
   TIMER_EVENT_STOP|basechange <eps>
BMCHANGE BMEND:
   ${basemotionid}==0 MOTION_CHANGE|0|base|${motion_dir}/01_Wait_b.vmd ${basemotionid}=1
BMCHANGE BMEND:
   ${basemotionid}==1 MOTION_CHANGE|0|base|${motion_dir}/wait_moving.vmd ${basemotionid}=2
BMCHANGE BMEND:
   ${basemotionid}==2 MOTION_CHANGE|0|base|${motion_dir}/01_Wait.vmd ${basemotionid}=0
BMEND LOOP:
   <eps> TIMER_START|basechange|${base_duration}
