'''
The GUI for the client. This has no functionality; it simply
deals with the display.
'''

import tkinter as tk
import client.readonlytext as rot

class ChatClientGui:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(0, 0)
        
        self.entry_frame = EntryFrame(self.root)
        self.entry_frame.pack(side=tk.BOTTOM, fill="x", padx="3m", pady="3m", ipadx="2m")
        
        self.display_frame = DisplayFrame(self.root)
        self.display_frame.pack(side=tk.BOTTOM, padx="3m", pady="3m")
        
        self.status_frame = StatusFrame(self.root)
        self.status_frame.pack(side=tk.BOTTOM, fill="x", padx="3m", pady="3m")
        
class EntryFrame(tk.Frame):
    
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.send_button = tk.Button(self, text="Send", width=10)
        self.msg_entry = tk.Entry(self, width=90)
        self.send_button.pack(side=tk.RIGHT)
        self.msg_entry.pack(side=tk.LEFT)
        
class DisplayFrame(tk.Frame):
    
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw) 
        self.text = rot.ReadOnlyText(self, wrap=tk.WORD)
        self.text.pack()
        
class StatusFrame(tk.Frame):
    
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        
        self.host_entry = tk.Entry(self)
        self.host_entry.pack(side=tk.LEFT)
        self.port_entry = tk.Entry(self)
        self.port_entry.pack(side=tk.LEFT)
        self.connect_button = tk.Button(self, text="Connect")
        self.connect_button.pack(side=tk.LEFT)
        
        self.name_button = tk.Button(self, text="Set name")
        self.name_button.pack(side=tk.RIGHT)        
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(side=tk.RIGHT)        
