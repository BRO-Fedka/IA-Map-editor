from tkinter import *


class FileMenu(Menu):
    def __init__(self):
        super().__init__()
        self.add_command(label="New")
        self.add_command(label="Open")
        self.add_command(label="Save")
        self.entryconfig("Save", state="disabled")
        self.add_command(label="Save as")
        self.entryconfig("Save as", state="disabled")
        self.add_separator()
        self.add_command(label="Preview")
        self.entryconfig("Preview", state="disabled")
        self.add_separator()
        self.add_command(label="Exit", command=exit)
