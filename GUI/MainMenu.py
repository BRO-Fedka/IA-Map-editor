from GUI.IAMenu import *
from GUI.FileMenu import *


class MainMenu(IAMenu):
    def __init__(self):
        super().__init__()
        self.add_cascade(label="File", menu=FileMenu())

