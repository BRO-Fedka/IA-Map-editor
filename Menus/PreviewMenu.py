from Menus.IAMenu import *
from tkinter import filedialog
from Map.Map import *
from Forms.PreviewForm import *
from Forms.NewForm import *
import sys


class PreviewMenu(IAMenu):

    def __init__(self):
        super().__init__()
        self.add_command(label="*.SVG", command=self.svg)
        self.add_separator()
        self.add_command(label="Other", command=self.other)

    def svg(self):
        try:
            self.get_workspace().get_map().get_preview_image_svg()
        except:
            pass

    def other(self):
        a = PreviewForm(self)

