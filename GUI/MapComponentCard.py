from tkinter import *
from typing import *
from Logic.MapComponent import *


class MapComponentCard(Frame):
    __map_component: MapComponent = None
    __photo_image: PhotoImage = None
    __lbl_image: Label = None
    __lbl_name: Label = None
    __hoverbg: str = "#0088ff"
    __bg: str = "#ffffff"

    def __init__(self, master: Optional[Misc], map_component: MapComponent, **kwargs):
        self.__map_component = map_component
        if 'hoverbg' in kwargs:
            self.__hoverbg = kwargs['hoverbg']
            kwargs.pop('hoverbg')
        if 'bg' in kwargs:
            self.__bg = kwargs['bg']
        else:
            kwargs['bg'] = self.__bg
        super().__init__(master, kwargs)
        self['width'] = 100
        self['height'] = 120
        self.__photo_image = map_component.get_card_icon()
        self.__lbl_image = Label(self, image=self.__photo_image, bg=self.__bg)
        self.__lbl_image.place(x=0, y=0)
        self.__lbl_name = Label(self, bg=self.__bg, text="Example")
        self.__lbl_name.place(anchor=S, relx=0.5, rely=1)
        self.bind('<Enter>', self.__enter)
        self.bind('<Leave>', self.__leave)

    def __enter(self, event):
        self['bg'] = self.__hoverbg
        self.__lbl_image.configure(bg=self.__hoverbg)
        self.__lbl_name.configure(bg=self.__hoverbg)

    def __leave(self, event):
        self['bg'] = self.__bg
        self.__lbl_image.configure(bg=self.__bg)
        self.__lbl_name.configure(bg=self.__bg)
