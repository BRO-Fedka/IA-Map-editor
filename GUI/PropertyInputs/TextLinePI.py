from tkinter import Entry, END
from GUI.PropertyInputs.IPropertyInput import IPropertyInput
from typing import Callable
import logging


class TextLinePI(Entry, IPropertyInput):

    def __init__(self, master, getter: Callable[[], float], setter: Callable[[float], None], **kwargs):
        kwargs['font'] = ('', 10)
        if not 'width' in kwargs: kwargs['width'] = 30
        kwargs['selectforeground'] = '#000'
        super().__init__(master, **kwargs)
        self.bind('<KeyRelease>', self.__valid)
        self.bind('<FocusIn>', self.__on_focus_in)
        self.bind('<FocusOut>', self.__on_focus_out)
        self._setter = setter
        self._getter = getter
        self.delete(0, END)
        self.value: float = getter()
        self.insert(0, str(self.value))
        self.__valid(None)
        self.__on_focus_out(None)

    def __valid(self, e):
        value = self.get()
        self._setter(value)
        self.value = self._getter()

    def __on_focus_in(self, e):
        self['bg'] = "#f88"

    def __on_focus_out(self, e):
        self['bg'] = "#fff"
