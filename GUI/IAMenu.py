from tkinter import *
from GUI import Workspace


class IAMenu(Menu):
    def get_workspace(self) -> Workspace:
        return self.master.get_workspace()
