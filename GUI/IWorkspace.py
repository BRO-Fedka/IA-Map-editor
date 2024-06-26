from tkinter import *
from Map.IMap import *


class Coords(NamedTuple):
    x: float
    y: float


class IWorkspace(Protocol):
    def __init__(self, master: Optional[Misc], **kwargs):
        pass

    def set_map(self, map: IMap):
        pass

    def update_map(self):
        pass

    def update_content(self):
        pass

    def calc_x(self, x: float) -> float:
        pass

    def calc_y(self, y: float) -> float:
        pass

    def set_zoom(self, zoom: float):
        pass

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def get_zoom(self) -> float:
        pass

    def move_view(self, x: float, y: float):
        pass

    def move_view_pix(self, x: int, y: int):
        pass

    def set_view(self, x: float, y: float):
        pass

    def get_view_x(self) -> float:
        pass

    def get_view_y(self) -> float:
        pass

    def get_game_coords_from_pix(self, x: int, y: int) -> Coords:
        pass

    def itemconfig(self, tag_or_id: [int,str], cnf=None, **kw):
        pass

    def lift(self, *args):
        pass


