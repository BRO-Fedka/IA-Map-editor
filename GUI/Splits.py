from tkinter import *
from typing import *
from GUI.ICommon import *


class SplitHorizontal(Frame,ICommon):
    __split_place: float = 0.5
    __is_split_held: bool = False
    __left_item: [Widget, None] = None
    __right_item: [Widget, None] = None
    __r_min_size: int = 10
    __l_min_size: int = 10

    def __init__(self, master: Optional[Misc], split_place: float, **kwargs):
        super().__init__(master, kwargs)
        self.__split_place = split_place
        self.bind('<Configure>', self.set_split_place)

    def set_left_widget(self, widget: Widget, min_size: int = 10, add_binds: bool = True):
        self.__left_item = widget
        self.__l_min_size = min_size
        widget.place(relx=0, relwidth=self.__split_place, rely=0, relheight=1)
        if add_binds:
            widget.bind('<Motion>', self.__on_motion_left_widget)
            widget.bind("<ButtonPress>", self.__on_press_left_widget)
            widget.bind("<ButtonRelease>", self.__on_release)

    def set_right_widget(self, widget: Widget, min_size: int = 10, add_binds: bool = True):
        self.__right_item = widget
        self.__r_min_size = min_size
        widget.place(relx=self.__split_place, relwidth=1 - self.__split_place, rely=0, relheight=1)
        if add_binds:
            widget.bind('<Motion>', self.__on_motion_right_widget)
            widget.bind("<ButtonPress>", self.__on_press_right_widget)
            widget.bind("<ButtonRelease>", self.__on_release)

    def set_split_place(self, split_place: float):
        if type(split_place) != float:
            split_place = self.__split_place
        if split_place < self.__l_min_size/self.winfo_width():
            split_place = self.__l_min_size/self.winfo_width()
        elif split_place > (self.winfo_width()-self.__r_min_size)/self.winfo_width():
            split_place = (self.winfo_width()-self.__r_min_size)/self.winfo_width()
        self.__split_place = split_place
        if self.has_left_widget():
            self.__left_item.place_configure(relx=0, relwidth=self.__split_place)
        if self.has_right_widget():
            self.__right_item.place_configure(relx=self.__split_place, relwidth=1 - self.__split_place)

    def get_left_widget(self) -> Widget:
        if not self.has_left_widget():
            raise Exception("Widget does not exist")
        return self.__left_item

    def get_right_widget(self) -> Widget:
        if not self.has_right_widget():
            raise Exception("Widget does not exist")
        return self.__right_item

    def has_left_widget(self) -> bool:
        if self.__left_item is None:
            return False
        else:
            return True

    def has_right_widget(self) -> bool:
        if self.__right_item is None:
            return False
        else:
            return True

    def delete_right_widget(self):
        if not self.has_right_widget():
            raise Exception("Widget has been already deleted")
        else:
            self.__right_item.place_forget()
            self.__right_item = None

    def delete_left_widget(self):
        if not self.has_left_widget():
            raise Exception("Widget has been already deleted")
        else:
            self.__left_item.place_forget()
            self.__left_item = None

    def __on_motion_right_widget(self, event):
        if event.x < 5:
            event.widget['cursor'] = 'sb_h_double_arrow'
        else:
            event.widget['cursor'] = 'arrow'
        if self.__is_split_held:
            event.widget['cursor'] = 'sb_h_double_arrow'
            self.set_split_place(self.__split_place+event.x/self.winfo_width())

    def __on_motion_left_widget(self, event):

        if abs(event.widget.winfo_width()-event.x) < 5:
            event.widget['cursor'] = 'sb_h_double_arrow'
        else:
            event.widget['cursor'] = 'arrow'
        if self.__is_split_held:
            event.widget['cursor'] = 'sb_h_double_arrow'
            self.set_split_place(event.x / self.winfo_width())

    def __on_press_right_widget(self, event):
        if event.x < 5:
            self.__is_split_held = True

    def __on_press_left_widget(self, event):
        if abs(event.widget.winfo_width()-event.x) < 5:
            self.__is_split_held = True

    def __on_release(self, event):
        self.__is_split_held = False
