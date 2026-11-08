#
# RECOG_EVENT_START: start speech recognition
# RECOG_EVENT_STOP: return recognized test
#
import pyaudio
import numpy as np
import DaemonClient
import threading
import queue
import time
import MMDA_connector

class SpRecognizer():
    @classmethod
    def print_mic_list(cls):
        p = pyaudio.PyAudio()
        print("\n----- mic device list ---")
        for i in range(0, p.get_device_count()):
            a = p.get_device_info_by_index(i)
            if a["maxInputChannels"] > 0:
                print("index: %d, name: %s" % (a["index"], a["name"]))
        p.terminate()

    def vad(self, timeout=5):
        while self.runFlg:
            vad_socket = DaemonClient.client(**self.vad_param)
            _ = self.run_q.get()
            self.mic_stream.start_stream()
            vad_socket.send_stream(np.array([self.gap, timeout], dtype=np.float32).tobytes())
            response = None
            while not self.suspendFlg:
                data = self.mic_stream.read(self.buffer_size)
                vad_socket.send_stream(data)
                response = vad_socket.recv_stream()
                if response is not None:
                    break
            if response is None:
                self.mic_stream.stop_stream()
                vad_socket.close_stream()
                self.wav_q.put((False, "forced stop"))
            else:
                if response["status"] == False:
                    self.wav_q.put((False, response["error_message"]))
                else:
                    self.wav_q.put((True, response["speech"]))
                self.run_q.put(0)
                
    def suspend_whisper(self):
        msg_data = [
            "CAPTION_START",
            "synth_voice",
            "synth_style",
            "",
            "2.5",
            "RIGHT",
            "0.6",
            "90"
            ]
            
        while self.runFlg:
            str = self.connector.get_msg()
            if str[0] == "SYNTH_START":
                self.suspend()
                msg_data[3] = str[3]
                self.connector.put_msg(msg_data)
            elif str[0] == "SYNTH_EVENT_STOP":
                time.sleep(0.5)
                self.resume()

    def recognize(self):
        result_flg, wav = self.wav_q.get()
        if result_flg:
            self.send_data["wav"] = wav
            response = self.asr_socket.send(self.send_data)
            if response["status"] == False:
                return (False, response["error_message"])
            else:
                return (True, response["text"])
        else:
            return (False, wav)

    def __init__(
            self,
            model="large",
            asr_server="150.89.239.210",
            asr_port=12103,
            vad_server="150.89.239.209",
            vad_port=12097,
            gap = 0.5,
            mic=None,
            source_lang="ja",
            target_lang="ja",
            save_wave=True,
            save_period=0,
            connector=None,
            ):
        self.sampling_rate = 16000
        self.send_data = {
            "model" : model,
            "sampling_rate" : self.sampling_rate,
            "language" : source_lang,
            "language" : target_lang,
            "task" : "transcribe",
        }
        self.asr_socket = DaemonClient.client(asr_server,asr_port)
                                        
        self.gap = gap
        self.buffer_size = 512
        mic_param = {
            "format" : pyaudio.paFloat32,
            "rate" : self.sampling_rate,
            "channels" : 1,
            "input_device_index" : mic,
            "input" : True,
            "frames_per_buffer" : self.buffer_size,
        }
        audio = pyaudio.PyAudio()
        self.mic_stream = audio.open(**mic_param)
        self.vad_param = {
            "host" : vad_server,
            "port" : vad_port,
            "stream_mode" : True,
        }
        self.run_q = queue.Queue()
        self.runFlg = False
        self.suspendFlg = False
        self.wav_q = queue.Queue()
        self.finalized = False
        self.connector = connector

    def start(self):
        if not self.runFlg:
            self.runFlg = True
            self.resume()
            self.suspend_thread = threading.Thread(target=self.suspend_whisper, daemon=True)
            self.suspend_thread.start()
            self.vad_thread = threading.Thread(target=self.vad, daemon=True)
            self.vad_thread.start()

    def suspend(self):
        self.suspendFlg = True

    def resume(self):
        self.suspendFlg = False
        self.run_q.put(0)
        
    def __del__(self):
        self.wait()
            
    def wait(self):
        if not self.finalized:
            self.runFlg = False
            self.suspend_thread.join()
            self.vad_thread.join()
            self.mic_stream.stop_stream()
            self.mic_stream.close()
        self.finalized = True

        
if __name__ == "__main__":
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--model', default="large", choices=["large", "turbo"], help="model name. large or small. (default: large)")
    argparser.add_argument('--mic_index', type=int, default=None, help="microphone device index")
    argparser.add_argument('--mic_device_list', action="store_true", help="print microphone device list")
    argparser.add_argument('--gap_threshold', type=float, default=0.5, help="short pause threshlold")
    argparser.add_argument('--source_lang', default="ja", help="spoken language")
    argparser.add_argument('--target_lang', default="ja", help="output (target) language")
    args = argparser.parse_args()
    
    if args.mic_device_list:
        SpRecognizer.print_mic_list()
        exit()

    connector = MMDA_connector.MMDA_connector()
    connector.listen("SYNTH_START")
    connector.listen("SYNTH_EVENT_STOP")
    connector.start()

    recognizer = SpRecognizer(
        model=args.model,
        gap=args.gap_threshold,
        mic=args.mic_index,
        source_lang=args.source_lang,
        target_lang=args.target_lang,
        connector=connector,
    )
    recognizer.start()
    connector.put_msg(["RECOG_EVENT_START"])
    msg_data = [
        "CAPTION_SETSTYLE",
        "whisper_style",
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
        "whisper",
        "whisper_style",
        "",
        "2.5",
        "LEFT",
        "0.4",
        "90"
        ]
    try:
        while True:
            flg, result = recognizer.recognize()
            if flg:
                connector.put_msg(["RECOG_EVENT_STOP", result])
                msg_data[3] = result
                connector.put_msg(msg_data)
    except KeyboardInterrupt:
        recognizer.wait()

