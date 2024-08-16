from tkinter import Entry, END
from GUI.PropertyInputs.IPropertyInput import IPropertyInput
from typing import Callable
import logging


class DirectionPI(Entry, IPropertyInput):
    _white_list = "0123456789"

    def __init__(self, master, getter: Callable[[], int], setter: Callable[[int], None], **kwargs):
        kwargs['font'] = ('', 10)
        kwargs['width'] = 3
        kwargs['justify'] = "center"
        kwargs['selectforeground'] = '#000'
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self.__valid)
        self.bind('<FocusIn>', self.__on_focus_in)
        self.bind('<FocusOut>', self.__on_focus_out)
        self.bind("<MouseWheel>", self.__on_mouse_wheel)
        self._setter = setter
        self._getter = getter
        self.delete(0, END)
        self.direction: int = getter()
        self.insert(0, str(self.direction))
        self.__valid(None)
        self.__on_focus_out(None)

    def __on_mouse_wheel(self, e):
        self.direction += round(e.delta/abs(e.delta))
        self.delete(0, END)
        self.insert(0, str(self.direction))
        self.__valid(None)

    def __valid(self, e):
        direction = self.get()
        if direction.count('-') > 0:
            direction = direction.replace('-', '')
        if not direction.isdigit():
            new_direction = ''
            for char in direction:
                if char in self._white_list:
                    new_direction += char
            if len(new_direction) == 0:
                direction = 0
            else:
                direction = int(new_direction)
        direction = round(int(direction))
        if direction < 0:
            direction = 0
        elif direction > 359:
            direction = 359
        self.delete(0, END)
        self.insert(0, str(direction))
        self._setter(direction)
        self.value = self._getter()
        self.direction = direction

    def __on_focus_in(self, e):
        self['bg'] = "#f88"

    def __on_focus_out(self, e):
        self['bg'] = "#fff"
