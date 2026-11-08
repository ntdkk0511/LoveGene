#
# まばたき用サブFST
#

${blink_interval}=4
${motion_dir}=../../Lib/motions/action

0 LOOP:
   <eps> TIMER_START|blink|${blink_interval}

# 一定時間ごとにまばたきする
LOOP LOOP:
   TIMER_EVENT_STOP|blink MOTION_ADD|0|blink|${motion_dir}/blink.vmd|PART|ONCE|ON|OFF
   MOTION_EVENT_ADD|0|blink MOTION_CONFIGURE|0|blink|MODE_MUL
   <eps> TIMER_START|blink|${blink_interval}
