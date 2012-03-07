'''
This class is the part of the client
which does the network stuff.
'''

import socket

class ChatClientSock:
    
    def __init__(self):
        self.host_addr = ('', 0)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def set_host(self, host, port):
        self.host_addr = (host, port)
        
    def connect(self):
        self.sock.connect(self.host_addr)
        
    def send(self, cmd, message):
        self.sock.send("{} {}".format(cmd, message).encode())

    def receive(self):
        try:
            return self.sock.recv(4096).decode()
        except:
            return None
                