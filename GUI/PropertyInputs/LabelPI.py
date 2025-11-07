from tkinter import Entry, END
from GUI.PropertyInputs.IPropertyInput import IPropertyInput
from typing import Callable, Any
import logging


class LabelPI(Entry, IPropertyInput):

    def __init__(self, master, getter: Callable[[], Any], setter: Any, **kwargs):
        kwargs['font'] = ('', 10)
        if not 'width' in kwargs: kwargs['width'] = 3
        kwargs['selectforeground'] = '#000'
        kwargs['fg'] = '#000'
        super().__init__(master, **kwargs)
        self._getter = getter
        self.delete(0, END)
        self.value: str = str(getter())
        self.insert(0, str(self.value))
        self['state'] = 'disabled'
