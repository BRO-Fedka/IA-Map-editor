from tkinter import *
from typing import *


class Workspace(Canvas):
    def __init__(self, master: Optional[Misc], **kwargs):
        super().__init__(master, kwargs)
        self['highlightthickness'] = 0
