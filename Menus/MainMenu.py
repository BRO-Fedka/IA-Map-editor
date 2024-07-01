from Menus.FileMenu import *
from GUI.ICommon import *


class MainMenu(IAMenu, ICommon):
    def __init__(self):
        super().__init__()
        self.add_cascade(label="File", menu=FileMenu())
