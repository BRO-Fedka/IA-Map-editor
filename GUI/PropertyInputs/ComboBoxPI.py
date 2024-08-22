from tkinter.ttk import Combobox
from GUI.PropertyInputs.IPropertyInput import IPropertyInput
from typing import Callable


class ComboBoxPI(Combobox, IPropertyInput):

    def __init__(self, master, getter: Callable[[], str], setter: Callable[[str], None], **kwargs):
        kwargs['font'] = ('', 9)
        self._values = kwargs['values']
        super().__init__(master, **kwargs)
        self._setter = setter
        self._getter = getter
        self.set(getter())
        self.bind("<<ComboboxSelected>>", self.__on_value_changed)

    def __on_value_changed(self, e=None):
        self._setter(self.get())
        self.set(self._getter())
