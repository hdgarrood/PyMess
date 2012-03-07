'''
Subclass of Tkinter's Text class with a new write()
method which feigns a read-only text widget, by
enabling the area before writing and immediately
disabling afterwards.
'''

import tkinter.scrolledtext as st
import tkinter.constants as tkc

class ReadOnlyText(st.ScrolledText):
    
    def __init__(self, master=None, **kw):
        super().__init__(master, **kw)
        self.configure(state=tkc.DISABLED)
    
    def write(self, chars):
        self.configure(state=tkc.NORMAL)
        self.insert(tkc.END, chars)
        self.configure(state=tkc.DISABLED)
