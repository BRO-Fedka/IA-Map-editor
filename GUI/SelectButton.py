from tkinter import *
from typing import *


class SelectButton(Button):
    __vals: List[Any] = None
    __cur_id: int = None

    def __init__(self, master: Optional[Misc], vals=List[Any], default: Any = None, **kwargs):
        kwargs['command'] = self.__on_click
        super().__init__(master, **kwargs)
        self.__vals = vals
        self.__cur_id = 0
        if not default is None:
            self.__cur_id = self.__vals.index(default)
        self['text'] = self.__vals[self.__cur_id]

    def __on_click(self):
        self.__cur_id = (self.__cur_id + 1) % len(self.__vals)
        self['text'] = self.__vals[self.__cur_id]

    def get(self) -> Any:
        return self.__vals[self.__cur_id]
