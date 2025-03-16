from GUI.IWorkspace import IWorkspace
from shapely.geometry import Point, Polygon
from typing import Tuple, List, Dict, Union
from PIL import ImageDraw
from svgwrite import Drawing
from Map.IMap import IMap
from functions.functions import hex_to_rgb
from svgwrite.shapes import Polygon as SVG_Polygon
import math
from Map.MapComponents.Buildings.BaseBuilding import BaseBuilding


class DirectedBuilding(BaseBuilding):
    type_id: int = None
    _map_ct: str = 'bg'
    _len_dirmark: float = None

    def __init__(self, workspace: IWorkspace, x: float, y: float, w: float, h: float, direction: int, map: IMap):
        self._dirmark_id = workspace.create_line(0, 0, 0, 0, fill="#f00",
                                                 tags=type(self).__name__)
        super().__init__(workspace, x, y, w, h, direction, map)

    def update(self):
        super().update()
        # print(dir(self))
        self._workspace.coords(self._dirmark_id, self._workspace.calc_x(self.x), self._workspace.calc_y(self.y),
                               self._workspace.calc_x(
                                   self.x + self._len_dirmark * math.cos(self._direction * math.pi / 180)),
                               self._workspace.calc_y(
                                   self.y + self._len_dirmark * math.sin(self._direction * math.pi / 180)))

    def select(self):
        super().select()
        self._workspace.itemconfig(self._dirmark_id, fill="#f00")

    def unselect(self):
        super().unselect()
        self._workspace.itemconfig(self._dirmark_id, fill="")

    def delete(self):
        super().delete()
        self._workspace.delete(self._dirmark_id)
