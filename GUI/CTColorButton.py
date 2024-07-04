from tkinter import *
from typing import *
from GUI.IField import *
from tkinter import colorchooser


class CTColorButton(Button, IField):
    __vals: List[Any] = None
    __cur_id: int = None
    __color: List[Union[float, int]] = None

    def __init__(self, master: Optional[Misc], key: str, color: str, setter: Callable, **kwargs):
        kwargs['command'] = self.__on_click
        kwargs['bg'] = '#ffffff'
        kwargs['text'] = '      '
        super().__init__(master, **kwargs)
        self.__key = key
        self.__setter = setter
        self.__set_color(color)

    def __on_click(self):
        cl = colorchooser.askcolor(parent=self)
        self.__set_color(str(cl[1]))
        self.__setter(self.__key,self.get())

    def get(self, need_hex: bool = False) -> str:
        if len(self.__color) == 3:
            return "#%02x%02x%02x" % tuple(self.__color)
        else:
            return 'rgba'+str(tuple(self.__color))

    def __set_color(self, val: str):
        print(val)
        if val[0] == '#':
            if self.__color is None:
                self.__color = [0, 0, 0]
            if len(val) == 4:
                self.__color[0] = int(val[1], 16) * 17
                self.__color[1] = int(val[2], 16) * 17
                self.__color[2] = int(val[3], 16) * 17

            elif len(val) == 7:
                self.__color[0] = int(val[1] + val[2], 16)
                self.__color[1] = int(val[3] + val[4], 16)
                self.__color[2] = int(val[5] + val[6], 16)

        elif val.count('rgba') != 0:
            def f(v: str):
                if v.count('.') > 0:
                    return float(v)
                else:
                    return int(v)

            self.__color = list(map(f, val.replace('rgba', '').replace(')', '').replace('(', '').split(',')))
        cls = self.__color.copy()
        if len(cls)>3:
            cls.pop(3)
        # print("#%02x%02x%02x" % tuple(cls))
        try:
            self['bg'] = "#%02x%02x%02x" % tuple(cls)
        except:pass
