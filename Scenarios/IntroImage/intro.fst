#
${libdir}=../../Lib
#
0 LOOP:
    <eps> STAGE|${libdir}/images/floor_green.png,${libdir}/images/back_white.png
    <eps> MODEL_ADD|0|${libdir}/gene/Gene.pmd
    MODEL_EVENT_ADD|0  MOTION_ADD|0|base|${libdir}/motions/wait/01_Wait.vmd|FULL|LOOP|ON|OFF
    <eps> CAMERA|0,15.25,0|4.5,0,0|22.4|27.0

LOOP LOOP:
    KEY|1 SYNTH_START|0|mei_voice_normal|こんにちは！よろしくね！

LOOP LOOP:
    KEY|2 SYNTH_START|0|slt_voice_normal|"Hello! My name is gene. How can I help you?"

#%INCLUDE(introimage.fst)  #演習用に追加


%INCLUDE(love.fst)
