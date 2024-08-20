from tkinter import Button
from GUI.PropertyInputs.IPropertyInput import IPropertyInput
from typing import Callable
from tkinter import colorchooser


class ColorPI(Button, IPropertyInput):

    def __init__(self, master, getter: Callable[[], str], setter: Callable[[str], None], **kwargs):
        kwargs['font'] = ('', 7)
        kwargs['width'] = 3
        kwargs['text'] = "   "
        kwargs['command'] = self.__on_click
        super().__init__(master, **kwargs)
        self._setter = setter
        self._getter = getter
        self['bg'] = getter()

    def __on_click(self, e=None):
        result = colorchooser.askcolor(title="Choose color")
        if not result is None:
            self._setter(result[1])
            self['bg'] = self._getter()