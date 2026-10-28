#
# Dummy Recognizer
#
import sys
import MMDA_connector

def show_synth_text(connector, msg):
    synth_msg_data[3] = msg[3]
    connector.put_msg(synth_msg_data)

captionFlg = len(sys.argv) > 1 and sys.argv[1] == "-c"
connector = MMDA_connector.MMDA_connector(tcpip=True)

if captionFlg:
    msg_data = [
        "CAPTION_SETSTYLE",
        "dummy_style",
        "default",
        "1,1,0,1",
        "0,0,0,0,0",
        "0,0,0,0,0",
        "0.2,0.2,0.2,0.2,1"
    ]
    connector.put_msg(msg_data)
    msg_data[1] = "synth_style"
    msg_data[3] = "0,1,1,1"
    connector.put_msg(msg_data)

    msg_data = [
        "CAPTION_START",
        "dummy_recognizer",
        "dummy_style",
        "",
        "2.5",
        "LEFT",
        "0.4",
        "90"
    ]

    synth_msg_data = [
        "CAPTION_START",
        "synth_voice",
        "synth_style",
        "",
        "2.5",
        "RIGHT",
        "0.6",
        "90"
    ]

if captionFlg:
    connector.add_handler("SYNTH_START", show_synth_text)
    connector.mainloop(block=False)
else:
    connector.start(listen=False)

while connector.available():
    str = input().strip()
    if not str:
        break
    if captionFlg:
        msg_data[3] = str
        connector.put_msg(msg_data)
    connector.put_msg(["RECOG_EVENT_STOP", str])

