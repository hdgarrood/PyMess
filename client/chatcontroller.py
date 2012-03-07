'''
This class is the glue between the ChatClientGui and the ChatClientSock
classes. It sets up the button bindings, and the separate thread so that
messages can be received in real-time without affecting the responsiveness
of the GUI.
'''

import threading
import time
import tkinter.constants as tkc
from client import chatgui, chatsock

class ChatClientController:
    
    def __init__(self):
        self.gui = chatgui.ChatClientGui()
        self.connected = False
        
        # Receive messages in a separate thread
        self.receiving_thread = threading.Thread(target=self.receive)
        self.receiving_thread.daemon = True
        
        # Button bindings
        self.gui.entry_frame.msg_entry.bind('<Return>', self.send)
        self.gui.entry_frame.send_button.bind('<Button-1>', self.send)
        self.gui.status_frame.connect_button.bind('<Button-1>', self.connect_or_disconnect)
        self.gui.status_frame.name_button.bind('<Button-1>', self.rename)
        
    def connect_or_disconnect(self, *args):
        if self.connected:
            self.disconnect()
            self.gui.status_frame.connect_button.configure(text="Connect")
        else:
            self.connect()
            self.gui.status_frame.connect_button.configure(text="Disconnect")
        
    def connect(self):
        host = self.gui.status_frame.host_entry.get()
        port = int(self.gui.status_frame.port_entry.get())
        self.sock = chatsock.ChatClientSock()
        self.sock.set_host(host, port)
        self.sock.connect()
        self.connected = True
        self.gui.status_frame.host_entry.configure(state=tkc.DISABLED)
        self.gui.status_frame.port_entry.configure(state=tkc.DISABLED)
        
    def disconnect(self):
        self.sock.sock.close
        del self.sock
        self.connected = False
        self.gui.status_frame.host_entry.configure(state=tkc.NORMAL)
        self.gui.status_frame.port_entry.configure(state=tkc.NORMAL)
        
    def send(self, *args):
        if self.connected:
            message = self.gui.entry_frame.msg_entry.get()
            self.sock.send("say", message)
            self.gui.entry_frame.msg_entry.delete(0,tkc.END)
            
    def rename(self, *args):
        if self.connected:
            name = self.gui.status_frame.name_entry.get()
            self.sock.send("name", name)
        
    def receive(self):
        while True:
            if self.connected:
                string = self.sock.receive()
                if string:
                    self.gui.display_frame.text.write(string)
                    self.gui.display_frame.text.yview(tkc.END)
            time.sleep(0.3)
        
    def run(self):
        self.receiving_thread.start()
        self.gui.root.mainloop()
