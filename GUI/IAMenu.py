from tkinter import *
from GUI import IWorkspace


class IAMenu(Menu):
    def get_workspace(self) -> IWorkspace:
        return self.master.get_workspace()
