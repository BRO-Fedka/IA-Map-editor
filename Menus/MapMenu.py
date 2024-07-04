from Menus.IAMenu import *
from Forms.CTConfigForm import *
from tkinter import filedialog


class MapMenu(IAMenu):
    __file_types = (
        ('json files', '*.json'),
        ('All files', '*.*')
    )

    def __init__(self):
        super().__init__()
        self.add_command(label="Configure CT", command=self.config_ct)
        self.add_command(label="Load CT", command=self.load_ct)
        self.add_command(label="Save CT", command=self.save_ct)

    def config_ct(self):
        a = CTConfigForm(self)

    def save_ct(self):
        if self.get_workspace().get_map() is None:
            return
        fp = filedialog.asksaveasfilename(defaultextension="json", filetypes=self.__file_types,initialfile="ct.json")
        if fp != "":
            self.get_workspace().get_map().save_ct(fp)

    def load_ct(self):
        if self.get_workspace().get_map() is None:
            return
        fp = filedialog.askopenfilename(defaultextension="json", filetypes=self.__file_types)
        if fp != "":
            self.get_workspace().get_map().load_ct(fp)

