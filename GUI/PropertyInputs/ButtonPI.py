from tkinter import Button
from GUI.PropertyInputs.IPropertyInput import IPropertyInput
from typing import Callable


class ButtonPI(Button, IPropertyInput):

    def __init__(self, master, getter: Callable, setter: Callable, **kwargs):
        kwargs['font'] = ('', 7)
        super().__init__(master, **kwargs)
