from tkinter import Entry, END
from GUI.PropertyInputs.IPropertyInput import IPropertyInput
from typing import Callable
import logging


class CharPI(Entry, IPropertyInput):
    _white_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, master, getter: Callable[[], str], setter: Callable[[str], None], **kwargs):
        kwargs['font'] = ('', 10)
        kwargs['width'] = 2
        kwargs['justify'] = "center"
        kwargs['selectforeground'] = '#000'
        super().__init__(master, **kwargs)
        self.bind('<Key>', self.__on_key)
        self.bind('<FocusIn>', self.__on_focus_in)
        self.bind('<FocusOut>', self.__on_focus_out)
        self._setter = setter
        self._getter = getter
        self.delete(0, END)
        self.insert(0, getter())
        self.__on_focus_out(None)

    def __on_key(self, e):
        char = str(e.char).upper()
        if char in self._white_list:
            self.delete(0, END)
            self.insert(0, char)
            try:
                self._setter(char)
                self.delete(0, END)
                self.insert(0, self._getter())
            except:
                logging.exception('')

        return 'break'

    def __on_focus_in(self, e):
        self['insertbackground'] = '#f88'
        self['selectbackground'] = '#f88'
        self['bg'] = "#f88"

    def __on_focus_out(self, e):
        self['insertbackground'] = '#fff'
        self['selectbackground'] = '#fff'
        self['bg'] = "#fff"
