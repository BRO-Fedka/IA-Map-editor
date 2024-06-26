from typing import *
from tkinter import *


class IInfoBar(Protocol):
    def __init__(self, master: Optional[Misc], **kwargs):
        pass

    def update_x(self,val: float):
        pass

    def update_y(self,val: float):
        pass

    def update_wh(self,val: float):
        pass
