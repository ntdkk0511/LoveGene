#
# MMDAgent connector
#
import socket
import threading
import sys
import io
import queue
import time

class MMDA_connector:
    def __init__(self, server="localhost", port=50001, tcpip=False):
        self.tcpip = tcpip
        if tcpip:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((server, port))
            self.remain = ""
        else:
            sys.stdin=io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
            sys.stdout=io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        self.handler = {}
        self.listen_msg = set()
        self.msg_q = queue.Queue()
        self.runFlg = False

    def msg_recv(self):
        while self.runFlg:
            if self.tcpip:
                try:
                    str = self.remain + self.client.recv(4096).decode("UTF-8")
                except ConnectionResetError:
                    self.runFlg = False
                    self.msg_q.put("MMDAgent is terminated.")
                    return
                msg = str.split("\n")
                if str[-1] != "\n":
                    self.remain = msg.pop()
            else:
                msg = [input().strip()]
            for m in msg:
                if m != '':
                    m_ary = m.split("|")
                    if len(self.listen_msg) == 0 or m_ary[0] in self.listen_msg:
                        self.msg_q.put(m_ary)

    def start(self, listen=True):
        self.runFlg = True
        if listen:
            self.msg_thread = threading.Thread(target=self.msg_recv, daemon=True)
            self.msg_thread.start()

    def get_msg(self, block=True):
        while True:
            try:
                return self.msg_q.get(block=False)
            except queue.Empty:
                if block:
                    time.sleep(0.1)
                    pass
                else:
                    return None
    
    def listen(self, msg):
        if msg == "all":
            self.listen_msg.clear()
        else:
            self.listen_msg.add(msg)
            
    def add_handler(self, msg, handler):
        self.listen(msg)
        self.handler[msg] = handler

    def boot_handler(self):
        while self.runFlg:
            try:
                msg = self.get_msg()
                if msg[0] in self.handler:
                    self.handler[msg[0]](self, msg)
            except KeyboardInterrupt:
                break
        
    def mainloop(self, block=True):
        if not self.runFlg:
            self.start()
        if block:
            self.boot_handler()
        else:
            self.mainloop_thread = threading.Thread(target=self.boot_handler, daemon=True)
            self.mainloop_thread.start()
                    
    def available(self):
        return self.runFlg
        
    def put_msg(self, data):
        msg = "|".join(data) + "\n"
        if self.tcpip:
            self.client.send(msg.encode("UTF-8"))
        else:
            print(msg, flush=True)

if __name__ == "__main__":
    connector = MMDA_connector(tcpip=True)
    args = sys.argv
    args.pop(0)
    for msg in args:
        connector.listen(msg)
    connector.start()
    while connector.available():
        try:
            print(connector.get_msg())
        except KeyboardInterrupt:
            break
    
