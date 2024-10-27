from GUI.IWorkspace import IWorkspace
from shapely.geometry import Point, Polygon
from typing import Tuple, List, Dict, Union
from PIL import ImageDraw
from svgwrite import Drawing
from Map.IMap import IMap
from functions.functions import hex_to_rgb
from svgwrite.shapes import Polygon as SVG_Polygon
import math


class BaseBuilding:
    type_id: int = None
    _map_ct: str = 'bg'

    def _calc_xy(self, coords: Tuple[float, float]) -> Tuple[float, float]:
        return self.x + coords[0] * self._vx[0] + coords[1] * self._vy[0], self.y + coords[0] * self._vx[1] + coords[
            1] * self._vy[1]

    def __init__(self, workspace: IWorkspace, x: float, y: float, w: float, h: float, direction: int, map: IMap):
        self._object_id = workspace.create_polygon(0, 0, 0, 0, fill="#fff", outline='',
                                                   tags=type(self).__name__)
        self._workspace = workspace
        self.x = x
        self.y = y
        self._map = map
        self._w = w
        self._h = h
        self._is_selected = False
        self._size = 0
        self._shape = Polygon()
        self._poly_shape = []
        self._vx = (0, 0)
        self._vy = (0, 0)
        self._direction = direction
        self.set_direction(direction)
        self.set_w(w)
        self.set_h(h)
        self.update_shape()
        self.update_ct()

    def hide(self):
        self._workspace.itemconfig(self._object_id, state="hidden")

    def show(self):
        self._workspace.itemconfig(self._object_id, state="normal")

    def set_direction(self, val: int):
        self._direction = val
        self._vx = (math.cos(val / 180 * math.pi), math.sin(val / 180 * math.pi))
        self._vy = (-math.sin(val / 180 * math.pi), math.cos(val / 180 * math.pi))
        self.update_shape()

    def update_shape(self):
        self._poly_shape = [
            (-self._w / 2, -self._h / 2),
            (-self._w / 2, self._h / 2),
            (self._w / 2, self._h / 2),
            (self._w / 2, -self._h / 2)
        ]
        current_poly = list(map(self._calc_xy, self._poly_shape))
        self._shape = Polygon(current_poly)
        self.update()

    def get_direction(self) -> int:
        return self._direction

    def set_w(self, val: float):
        self._w = val
        self.update_shape()

    def set_h(self, val: float):
        self._h = val
        self.update_shape()

    def get_w(self) -> float:
        return self._w

    def get_h(self) -> float:
        return self._h

    def move(self, x: float, y: float):
        self.x += x
        self.y += y
        self.update_shape()
        self.update()

    def update_scale(self):
        pass

    def get_polygon(self) -> Polygon:
        return self._shape

    def draw_map_instance_image_draw(self, draw: ImageDraw.Draw, img_wh: int):
        map_wh = self._map.get_wh()

        def f(val):
            return round(val[0] / map_wh * img_wh), round(val[1] / map_wh * img_wh)

        draw.polygon(list(map(f, self._shape.exterior.coords[:])),
                     fill=hex_to_rgb(self._map.get_ct_field(self._map_ct)))

    def draw_map_instance_svgwrite(self, draw: Drawing, img_wh: int):
        map_wh = self._map.get_wh()

        def f(val):
            return (val[0] / map_wh * img_wh), (val[1] / map_wh * img_wh)

        poly = draw.add(SVG_Polygon(list(map(f, self._shape.exterior.coords[:]))))
        poly.fill(self._map.get_ct_field(self._map_ct))

    def get_as_list(self) -> List:
        # print([self.type_id, round(self.x, 2), round(self.y, 2), round(self._w, 2), round(self._h, 2),
        #         self.get_direction()])
        return [self.type_id, round(self.x, 2), round(self.y, 2), round(self._w, 2), round(self._h, 2),
                self.get_direction()]

    def update(self):
        poly_cords = []
        for coord in self._shape.exterior.coords[:]:
            poly_cords.append(self._workspace.calc_x(coord[0]))
            poly_cords.append(self._workspace.calc_y(coord[1]))
        self._workspace.coords(self._object_id, poly_cords)

    def update_ct(self):
        self._workspace.itemconfig(self._object_id, fill=self._map.get_ct_field(self._map_ct))

    def select(self):
        self._is_selected = True
        self._workspace.itemconfig(self._object_id, outline="#000")

    def unselect(self):
        self._is_selected = False
        self._workspace.itemconfig(self._object_id, outline="")

    def delete(self):
        self._workspace.delete(self._object_id)

