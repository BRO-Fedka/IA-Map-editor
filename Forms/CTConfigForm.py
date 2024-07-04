from tkinter import *
from GUI.ICommon import *
from GUI.SelectButton import *
from Map.Map import *
from tkinter.ttk import Scrollbar
from GUI.IField import *
from GUI.CTColorButton import *


class CTConfigForm(Toplevel, ICommon):
    __data: Dict[str, str]
    __fields: Dict[str, IField]

    def __init__(self, master, **kwargs):
        kwargs['bg'] = '#ddd'
        super().__init__(master, **kwargs)
        if self.get_workspace().get_map() is None:
            self.destroy()
            return
        self.attributes('-toolwindow', True)
        self.geometry('320x480')
        self.__data = self.get_workspace().get_map().get_ct_copy()
        self.__fields = {}

        self.__frm_field = Frame(self, bg=self['bg'])
        self.__frm_field.place(x=0, y=0, relwidth=1, relheight=1)
        self.__cnv_field = Canvas(self.__frm_field, bg=self['bg'], highlightthickness=0)
        self.__cnv_field.bind('<Configure>', self.__cnv_config)
        self.__scr_txt_field = Scrollbar(self.__frm_field, orient=VERTICAL, command=self.__cnv_field.yview)
        self.__scr_txt_field.pack(fill=Y, side=RIGHT)
        self.__cnv_field.pack(fill=BOTH)
        self.__cnv_field.config(yscrollcommand=self.__scr_txt_field.set)
        self.__frm_inner = Frame(self, bg=self['bg'])
        self.__cnv_field.create_window(0, 0, anchor=NW, window=self.__frm_inner)
        self.__cnv_config()
        self.__btn_save = Button(self, text="Save", command=self.__save)
        self.__btn_save.pack(side=BOTTOM, anchor=SE, padx=20, ipadx=20)
        i = 0
        for key in self.__data.keys():
            self.__add_field(key, i)
            i += 1
        self.title('CT Config')
        self.attributes("-topmost", True)

    def __cnv_config(self, event=None):
        self.__cnv_field.config(scrollregion=self.__cnv_field.bbox('all'))

    def __add_field(self, key: str, i: int):
        Label(self.__frm_inner, text=key, bg=self['bg']).grid(row=i, column=0, sticky=W, padx=5)
        if len(key) > 3:
            if key == "weather":
                self.__fields[key] = SelectButton(self.__frm_inner, ["Clear", "Snow"], width=8)
        else:
            self.__fields[key] = CTColorButton(self.__frm_inner, key, self.__data[key],
                                               self.get_workspace().get_map().set_ct_field)
        self.__fields[key].grid(row=i, column=1, sticky=EW, pady=5)

    def __save(self):
        for key in self.__data.keys():
            self.__data[key] = self.__fields[key].get()

    def destroy(self):
        for key in self.__data.keys():
            self.get_workspace().get_map().set_ct_field(key, self.__data[key])
        super().destroy()
