from typing import *
from tkinter import *
from Map.MapComponents.MCProperty import MCProperty

class IInfoBar(Protocol):
    def __init__(self, master: Optional[Misc], **kwargs):
        pass

    def update_x(self, val: float):
        pass

    def update_y(self, val: float):
        pass

    def update_wh(self, val: float):
        pass

    def update_selection(self, val: int):
        pass

    def show_properties(self, properties: List[MCProperty]):
        pass

    def hide_properties(self):
        pass