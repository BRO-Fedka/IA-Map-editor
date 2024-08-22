from tkinter import Entry, END
from GUI.PropertyInputs.IPropertyInput import IPropertyInput
from typing import Callable
import logging


class PositiveFloatPI(Entry, IPropertyInput):
    _white_list = "0123456789."

    def __init__(self, master, getter: Callable[[], float], setter: Callable[[float], None], **kwargs):
        self._ndigits = 2
        try:
            self._ndigits = kwargs['ndigits']
        except:
            pass
        kwargs['font'] = ('', 10)
        kwargs['width'] = 7
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
        self.value: float = getter()
        self.insert(0, str(self.value))
        self.__valid(None)
        self.__on_focus_out(None)

    def __on_mouse_wheel(self, e):
        self.value += (e.delta/abs(e.delta)*0.01)
        self.value = round(self.value, self._ndigits)
        self.delete(0, END)
        self.insert(0, str(self.value))
        self.__valid(None)

    def __valid(self, e):
        value = self.get()
        if value.count('-') > 0:
            value = value.replace('-', '')
        if value.count('.') > 1:
            value = '0'
        elif not value.isdigit():
            new_value = ''
            for char in value:
                if char in self._white_list:
                    new_value += char
            if len(new_value) == 0:
                value = 0
            else:
                value = float(new_value)
        value = round(float(value), self._ndigits)
        if value < 0:
            value = 0
        self.delete(0, END)
        self.insert(0, str(value))
        self._setter(value)
        self.value = self._getter()
        self.value = value

    def __on_focus_in(self, e):
        self['bg'] = "#f88"

    def __on_focus_out(self, e):
        self['bg'] = "#fff"
