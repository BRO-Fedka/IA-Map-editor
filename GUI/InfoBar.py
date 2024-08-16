from GUI.IInfoBar import *
from GUI.ICommon import *


class InfoBar(Frame, IInfoBar, ICommon):
    def __init__(self, master: Optional[Misc], **kwargs):
        super().__init__(master, kwargs)
        self['height'] = 20
        self.__lbl_x = Label(self, text='X:', bg=self['bg'], width=6, anchor="w")
        self.__lbl_x.pack(side=LEFT)
        # self.__lbl_x.grid(row=0, column=0)
        self.__lbl_y = Label(self, text='Y:', bg=self['bg'], width=6, anchor="w")
        self.__lbl_y.pack(side=LEFT)
        # self.__lbl_y.grid(row=0, column=1)
        self.__lbl_wh = Label(self, text='WH:', bg=self['bg'], width=6, anchor="w")
        self.__lbl_wh.pack(side=LEFT)
        # self.__lbl_wh.grid(row=0, column=2)
        self.__lbl_sel = Label(self, text='SEL:', bg=self['bg'], width=6, anchor="w")
        self.__lbl_sel.pack(side=LEFT)
        # self.__lbl_sel.grid(row=0, column=3)
        self.__frm_properties = Frame(self, bg=self['bg'], height=21)
        self.__frm_properties.pack(side=LEFT)
        self.__properties: List[List[Widget,Widget]] = []
        self.bind('<Button>', lambda e:self.focus_set())

    def update_x(self, val: float):
        self.__lbl_x['text'] = f"X: {val}"

    def update_y(self, val: float):
        self.__lbl_y['text'] = f"Y: {val}"

    def update_wh(self, val: float):
        self.__lbl_wh['text'] = f"WH: {val}"

    def update_selection(self, val: int):
        if val > 0:
            self.__lbl_sel['text'] = f"SEL: {val}"
        else:
            self.__lbl_sel['text'] = f"SEL:"

    def show_properties(self, properties: List[MCProperty]):
        for prop in properties:
            lbl = Label(self.__frm_properties, text=prop.name + ":", bg=self['bg'])
            lbl.pack(side=LEFT)
            pi = prop.widget(self.__frm_properties, getter=prop.getter, setter=prop.setter, **prop.kwards)
            pi.pack(side=LEFT)
            self.__properties.append([lbl, pi])

    def hide_properties(self):
        for prop in self.__properties:
            prop[0].pack_forget()
            prop[1].pack_forget()
        self.__properties = []