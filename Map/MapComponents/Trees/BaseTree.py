from GUI.IWorkspace import IWorkspace
from shapely.geometry import Point,Polygon
from typing import Tuple, List, Dict, Union
from PIL import ImageDraw
from svgwrite import Drawing
from Map.IMap import IMap
from functions.functions import hex_to_rgb
from svgwrite.shapes import Circle


class BaseTree:
    sizes_of_stages: Dict[int,float] = {}
    type_id: int = None
    _map_ct:str = 'tf'

    def __init__(self, workspace: IWorkspace, x: float, y: float, stage: int, map:IMap):
        self._workspace = workspace
        self.x = x
        self.y = y
        self._map = map
        self._stage = stage
        self._is_selected = False
        self._size = 0
        self.set_stage(stage)
        self.update_ct()

    def move(self, x: float, y: float):
        self.x += x
        self.y += y
        self.update()

    def get_stage(self) -> int:
        return self._stage

    def set_stage(self, val: Union[str, int]):
        val = int(val)
        if val in self.sizes_of_stages.keys():
            self._stage = val
            self._size = self.sizes_of_stages[val]
            self.update()

    def update(self):
        pass

    def update_ct(self):
        pass

    def update_scale(self):
        pass

    def select(self):
        self._is_selected = True

    def unselect(self):
        self._is_selected = False

    def get_as_buffered_point(self) -> Polygon:
        return Point(self.x, self.y).buffer(self._size / 2)

    def draw_map_instance_image_draw(self, draw: ImageDraw.Draw, img_wh: int):
        map_wh = self._map.get_wh()
        draw.ellipse((round((self.x - self._size / 2) / map_wh * img_wh),
                      round((self.y - self._size / 2) / map_wh * img_wh),
                      round((self.x + self._size / 2) / map_wh * img_wh),
                      round((self.y + self._size / 2) / map_wh * img_wh)), fill=hex_to_rgb(self._map.get_ct_field(self._map_ct)))

    def draw_map_instance_svgwrite(self, draw: Drawing, img_wh: int):
        map_wh = self._map.get_wh()
        circ = draw.add(Circle((self.x / map_wh * img_wh, self.y / map_wh * img_wh),
                               self._size / 2 / map_wh * img_wh))
        circ.fill(self._map.get_ct_field(self._map_ct))

    def get_as_list(self) -> List:
        return [self.type_id,round(self.x,2),round(self.y,2),self.get_stage()]

    def delete(self):
        pass
