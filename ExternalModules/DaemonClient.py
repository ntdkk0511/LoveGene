#!/usr/bin/env python

import socket
import pickle
import selectors

class client():
      rcv_buffer = 1024 * 1024
      int_bytes = 16
      
      def __init__(self, host, port, stream_mode=False):
            if stream_mode:
                  self.stream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  self.stream_socket.connect((host, port))
                  self.selector = selectors.DefaultSelector()
                  self.selector.register(self.stream_socket, selectors.EVENT_READ)
            else:
                  self.host = host
                  self.port = port

      def send(self, message):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                  sock.connect((self.host, self.port))
                  data = pickle.dumps(message)
                  sock.sendall(len(data).to_bytes(length=self.int_bytes, byteorder='big'))
                  sock.sendall(data)
                  return self.recv(sock)

      def recv(self, sock):
            received = b''
            rcv_data = sock.recv(self.int_bytes)
            data_size = int.from_bytes(rcv_data, byteorder='big')
            while data_size > len(received):
                  rcv_data = sock.recv(self.rcv_buffer)
                  received = received + rcv_data
            return pickle.loads(received)
            
      def recv_stream(self):
            ready = self.selector.select(0)
            if ready:
                  return self.recv(self.stream_socket)
            else:
                  return None
            
      def close_stream(self):
            self.stream_socket.shutdown(socket.SHUT_WR)
            
      def send_stream(self, data):
            self.stream_socket.sendall(data)
            
if __name__ == "__main__":

      import argparse
      import sys

      argparser = argparse.ArgumentParser()
      argparser.add_argument('-s', '--server', default="127.0.0.1", help="server name")
      argparser.add_argument('-p', '--port', type=int, default=12345, help="port number")
      args = argparser.parse_args()

      client_socket = client(args.server, args.port)
      data = {}
      while True:
            str = input(" >> ")
            if str == "":
                  break
            data["msg"] = str
            response = client_socket.send(data)
            print(" << " + response["msg"])


