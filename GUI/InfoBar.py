from GUI.IInfoBar import *
from GUI.ICommon import *

class InfoBar(Frame, IInfoBar, ICommon):
    def __init__(self, master: Optional[Misc], **kwargs):
        super().__init__(master, kwargs)
        self['height'] = 20
        self.__lbl_x = Label(self, text='X:', bg = self['bg'],width = 6, anchor="w")
        self.__lbl_x.grid(row=0, column=0)
        self.__lbl_y = Label(self, text='Y:', bg = self['bg'],width = 6, anchor="w")
        self.__lbl_y.grid(row=0, column=1)
        self.__lbl_wh = Label(self, text='WH:', bg = self['bg'],width = 6, anchor="w")
        self.__lbl_wh.grid(row=0, column=2)

    def update_x(self,val: float):
        self.__lbl_x['text'] = f"X: {val}"

    def update_y(self,val: float):
        self.__lbl_y['text'] = f"Y: {val}"

    def update_wh(self,val: float):
        self.__lbl_wh['text'] = f"WH: {val}"
