from Menus.IAMenu import *
from tkinter import filedialog
from Map.Map import *
from Forms.PreviewForm import *


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
        self.add_command(label="Preview", command=self.preview)
        # self.entryconfig("Preview", state="disabled")
        self.add_separator()
        self.add_command(label="Exit", command=exit)

    def open(self, event=None):
        fp = filedialog.askopenfilename(defaultextension='json')
        if fp != "":
            self.master.get_workspace().set_map(Map.from_json_file(fp, self.master.get_workspace()))

    def preview(self):
        a = PreviewForm(self)
