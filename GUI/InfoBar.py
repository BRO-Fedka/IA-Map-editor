from tkinter import *
from typing import *

class InfoBar(Frame):
    def __init__(self, master: Optional[Misc], **kwargs):
        super().__init__(master, kwargs)
        self['bg'] = "#ccc"
        self['height'] = 20


