from Menus.MainMenu import *
from GUI.InfoBar import *
from GUI.Splits import *
from GUI.MapComponentsMenu import *
from GUI.Workspace import *


class MainForm(Tk):
    def __init__(self):
        super().__init__()
        self.geometry('640x480')
        self['bg'] = "#ffffff"
        self.option_add("*tearOff", FALSE)
        self.__menu = MainMenu()
        self.config(menu=self.__menu)
        self.__info_bar = InfoBar(self, bg="#cccccc")
        self.__info_bar.pack(side=BOTTOM, fill=X)
        self.__split_frame = SplitHorizontal(self, 0.75, bg="#ffffff")
        self.__workspace = Workspace(self.__split_frame, bg="#eee")
        self.__map_component_menu = MapComponentsMenu(self.__split_frame, bg="#ddd")
        self.__split_frame.pack(fill=BOTH, expand=1)
        self.__split_frame.set_left_widget(self.__workspace, min_size=110, add_binds=False)
        self.__split_frame.set_right_widget(self.__map_component_menu, min_size=110)
        for map_component in get_finite_inherits(MapComponent):
            self.__map_component_menu.add_card(MapComponentCard(self.__map_component_menu, map_component))

    def get_workspace(self) -> Workspace:
        return self.__workspace

    def get_info_widget(self) -> InfoBar:
        return self.__info_bar

    def get_mc_menu(self) -> MapComponentsMenu:
        return self.__map_component_menu

