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


class CircularBuilding(BaseBuilding):
    type_id: int = None
    _map_ct: str = 'bg'

    def __init__(self, workspace: IWorkspace, x: float, y: float, w: float, h: float, direction: int, pi: int,
                 map: IMap):
        super().__init__(workspace, x, y, w, h, direction, pi, map)

    def set_w(self, val: float):
        self.set_d(val)

    def set_h(self, val: float):
        self.set_d(val)

    def set_d(self, val: float):
        self._w = val
        self._h = val
        self.update_shape()

    def update_shape(self):
        self._shape = Point(self.x, self.y).buffer(self._w / 2).simplify(0.2 * self._w / 2, preserve_topology=False)
        self.update()

    def get_as_list(self) -> List:
        if self.get_parent_id() == -1:
            return [self.type_id, round(self.x, 2), round(self.y, 2), round(self._w, 2)]
        else:
            return [self.type_id, round(self.x, 2), round(self.y, 2), round(self._w, 2), self.get_parent_id()]
