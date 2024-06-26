from GUI.IWorkspace import *
from GUI.IInfoBar import *
from GUI.IMapComponentsMenu import *


class ICommon:
    master = None

    def get_workspace(self) -> IWorkspace:
        return self.master.get_workspace()

    def get_info_widget(self) -> IInfoBar:
        return self.master.get_info_widget()

    def get_mc_menu(self) -> IMapComponentsMenu:
        return self.master.get_mc_menu()
