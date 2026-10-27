${lib_dir}=../../Lib

0 LOOP:
    <eps> STAGE|${lib_dir}/images/floor_block.png,${lib_dir}/images/back_white.png
    <eps> MODEL_ADD|gene|${lib_dir}/gene/Gene.pmd
    MODEL_EVENT_ADD|gene  MOTION_ADD|gene|base|walk.vmd|FULL|LOOP
    <eps> CAMERA|0,11.25,0|13.5,-50.0,0|46.4|27.0

LOOP LOOP:
    KEY|1 MOTION_ADD|gene|look|gaze.vmd|PART|ONCE

LOOP LOOP:
    KEY|2 MOTION_ADD|gene|greet|onehandwave.vmd|PART|ONCE


LOOP LOOP:
    KEY|3 MOTION_ADD|gene|hand|handupdown.vmd|FULL|ONCE