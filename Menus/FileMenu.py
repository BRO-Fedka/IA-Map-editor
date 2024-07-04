from Menus.IAMenu import *
from tkinter import filedialog
from Map.Map import *
from Forms.PreviewForm import *
from Forms.NewForm import *
import sys

class FileMenu(IAMenu):
    __file_types = (
        ('json files', '*.json'),
        ('All files', '*.*')
    )

    def __init__(self):
        super().__init__()
        self.add_command(label="New", command=self.new)
        self.add_command(label="Open", command=self.open)
        self.add_command(label="Save", command=self.save)
        # self.entryconfig("Save", state="disabled")
        self.add_command(label="Save as", command=self.save_as)
        # self.entryconfig("Save as", state="disabled")
        self.add_separator()
        self.add_command(label="Preview", command=self.preview)
        # self.entryconfig("Preview", state="disabled")
        self.add_separator()
        self.add_command(label="Exit", command=sys.exit)

    def open(self, event=None):
        fp = filedialog.askopenfilename(defaultextension="json", filetypes=self.__file_types)
        if fp != "":
            self.get_workspace().set_map(Map.from_json_file(fp, self.get_workspace()))

    def preview(self):
        a = PreviewForm(self)

    def new(self):
        a = NewForm(self)

    def save(self):
        if self.get_workspace().get_map() is None:
            return
        try:
            self.get_workspace().get_map().save_to_json_file()
        except ValueError:
            self.save_as()

    def save_as(self):
        if self.get_workspace().get_map() is None:
            return
        fp = filedialog.asksaveasfilename(defaultextension="json", initialfile="MAP.json", filetypes=self.__file_types)
        if fp != "":
            self.get_workspace().get_map().save_to_json_file(fp)
