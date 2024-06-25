from Map.MapComponents.MapComponent import *


class MapComponentCard(Frame):
    __map_component: Type[MapComponent] = None
    __photo_image: PhotoImage = None
    __lbl_image: Label = None
    __lbl_name: Label = None
    __hoverbg: str = "#aaaaaa"
    __bg: str = "#ffffff"
    __selectbg: str = "#0088ff"
    __is_selected: bool = False

    def __init__(self, master: Optional[Misc], map_component: Type[MapComponent], **kwargs):
        self.__map_component = map_component
        if 'selectbg' in kwargs:
            self.__selectbg = kwargs['selectbg']
            kwargs.pop('selectbg')
        if 'hoverbg' in kwargs:
            self.__hoverbg = kwargs['hoverbg']
            kwargs.pop('hoverbg')
        if 'bg' in kwargs:
            self.__bg = kwargs['bg']
        super().__init__(master, kwargs)
        if not ('bg' in kwargs):
            self.__bg = self.master['bg']
            self['bg'] = self.master['bg']
        self['width'] = 100
        self['height'] = 120
        self.__photo_image = map_component.get_card_icon()
        self.__lbl_image = Label(self, image=self.__photo_image, bg=self.__bg)
        self.__lbl_image.place(x=0, y=0)
        self.__lbl_name = Label(self, bg=self.__bg, text="Example")
        self.__lbl_name.place(anchor=S, relx=0.5, rely=1)
        self.bind('<Enter>', self.__enter)
        self.bind('<Leave>', self.__leave)
        self.bind('<Button-1>', self.__on_click)
        self.__lbl_image.bind('<Button-1>', self.__on_click)
        self.__lbl_name.bind('<Button-1>', self.__on_click)

    def __enter(self, event):
        if not self.is_selected():
            self['bg'] = self.__hoverbg
            self.__lbl_image['bg'] = self.__hoverbg
            self.__lbl_name['bg'] = self.__hoverbg

    def __leave(self, event):
        if not self.is_selected():
            self['bg'] = self.__bg
            self.__lbl_image['bg'] = self.__bg
            self.__lbl_name['bg'] = self.__bg

    def is_selected(self) -> bool:
        return self.__is_selected

    def select(self):
        self.__is_selected = True
        self['bg'] = self.__selectbg
        self.__lbl_image['bg'] = self.__selectbg
        self.__lbl_name['bg'] = self.__selectbg

    def unselect(self):
        self.__is_selected = False
        self['bg'] = self.__bg
        self.__lbl_image['bg'] = self.__bg
        self.__lbl_name['bg'] = self.__bg

    def __on_click(self,event):
        self.master.select(self)

    def get_map_component(self) -> MapComponent:
        return self.__map_component
