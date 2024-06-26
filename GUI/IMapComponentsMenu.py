from tkinter import *
from typing import *
from GUI.IMapComponentCard import *
from GUI.ICommon import *


class IMapComponentsMenu(Protocol):

    def __init__(self, master: Optional[Misc], **kwargs):
        pass

    def add_card(self, card: IMapComponentCard):
        pass

    def update_content(self):
        pass

    def place_configure(self, **kw):
        pass

    def select(self, card: IMapComponentCard):
        pass

    def get_selected_map_component(self) -> Type[MapComponent]:
        pass
