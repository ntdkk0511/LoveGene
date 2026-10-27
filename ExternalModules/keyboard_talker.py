#
# keyboard talker
#
import MMDA_connector

def sample_handler(connector, msg):
    sentence = {
        "1" : "私の名前は，ジェネです",
        "2" : "さようなら",
        "3" : "今日はいい天気ですね",
    }
    msg_data = ["SYNTH_START", "0", "mei_voice_normal"]
    if msg[1] in sentence:
        msg_data.append(sentence[msg[1]])
    else:
        msg_data.append("定義されていません")
    connector.put_msg(msg_data)

connector = MMDA_connector.MMDA_connector(tcpip=True)
connector.add_handler("KEY", sample_handler)

connector.mainloop()
