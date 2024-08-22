from GUI.IWorkspace import IWorkspace
from shapely.geometry import Point,Polygon
from typing import Tuple, List, Dict, Union
from PIL import ImageDraw
from svgwrite import Drawing
from Map.IMap import IMap


class BaseTree:
    sizes_of_stages: Dict[int,float] = {}
    type_id: int = None

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
        pass

    def draw_map_instance_svgwrite(self, draw: Drawing, img_wh: int):
        pass

    def get_as_list(self) -> List:
        return [self.type_id,round(self.x,2),round(self.y,2),self.get_stage()]

    def delete(self):
        pass
