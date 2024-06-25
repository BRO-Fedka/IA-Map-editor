from GUI.MainMenu import *
from GUI.InfoBar import *
from GUI.Splits import *
from GUI.MapComponentsMenu import *
from Map.MapComponents.MapComponent import *


class MainForm(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('640x480')
        self['bg'] = "#ffffff"
        self.option_add("*tearOff", FALSE)
        self.__menu = MainMenu()
        self.config(menu=self.menu)
        self.__info_bar = InfoBar(self)
        self.__info_bar.pack(side=BOTTOM, fill=X)
        self.__split_frame = SplitHorizontal(self, 0.75, bg="#ffffff")
        self.__workspace = Workspace(self.split_frame, bg="#eee")
        self.__map_component_menu = MapComponentsMenu(self.split_frame, bg="#ddd")
        self.__split_frame.pack(fill=BOTH, expand=1)
        self.__split_frame.set_left_widget(self.workspace, min_size=110, add_binds=False)
        self.__split_frame.set_right_widget(self.map_component_menu, min_size=110)
        self.__map_component_menu.add_card(MapComponentCard(self.map_component_menu, MapComponent))
        self.__map_component_menu.add_card(MapComponentCard(self.map_component_menu, MapComponent))
        self.__map_component_menu.add_card(MapComponentCard(self.map_component_menu, MapComponent))
        self.__map_component_menu.add_card(MapComponentCard(self.map_component_menu, MapComponent))

    def get_workspace(self) -> Workspace:
        return self.workspace
