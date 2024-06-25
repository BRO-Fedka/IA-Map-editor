from GUI.IAMenu import *
from tkinter import filedialog
from typing import *
from Map.Map import *


class FileMenu(IAMenu):
    def __init__(self):
        super().__init__()
        self.add_command(label="New")
        self.add_command(label="Open", command=self.open)
        self.add_command(label="Save")
        self.entryconfig("Save", state="disabled")
        self.add_command(label="Save as")
        self.entryconfig("Save as", state="disabled")
        self.add_separator()
        self.add_command(label="Preview")
        self.entryconfig("Preview", state="disabled")
        self.add_separator()
        self.add_command(label="Exit", command=exit)

    def open(self, event: Optional):
        fp = filedialog.askopenfilename(defaultextension='json')
        if fp != "":
            self.master.get_workspace().set_map(Map.from_json_file(fp))
