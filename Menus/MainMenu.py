from Menus.FileMenu import FileMenu, IAMenu
from GUI.ICommon import ICommon
from Menus.MapMenu import MapMenu
from Menus.PreviewMenu import PreviewMenu


class MainMenu(IAMenu, ICommon):
    def __init__(self):
        super().__init__()
        self.add_cascade(label="File", menu=FileMenu())
        self.add_cascade(label="Map", menu=MapMenu())
        self.add_cascade(label="Preview", menu=PreviewMenu())
