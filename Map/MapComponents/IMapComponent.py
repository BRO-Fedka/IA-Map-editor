from typing import *
from shapely.geometry import base
from Map.IMap import *
from GUI.IWorkspace import *
from PIL import Image,ImageDraw

class IMapComponent(Protocol):
    def __init__(self, workspace: IWorkspace, shape: base.BaseGeometry, map: IMap):
        pass

    def delete(self):
        pass

    def update_instance_ct(self):
        pass

    @classmethod
    def update_ct(cls):
        pass

    @classmethod
    def update(cls):
        pass

    def update_instance(self):
        pass

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map: IMap):
        pass

    @classmethod
    def lift(cls):
        pass

    def lift_instance(self):
        pass

    @classmethod
    def new_component(cls, workspace: IWorkspace, shape: base.BaseGeometry, map: IMap, **kwargs):
        pass

    @staticmethod
    def get_card_icon():
        pass

    @classmethod
    def get_card_name(cls):
        pass

    @classmethod
    def select_at_coords(cls, x: float, y: float):
        pass

    def intersects(self, shape: base.BaseGeometry) -> bool:
        pass

    def select(self):
        pass

    def unselect(self):
        pass

    @classmethod
    def remove_all_selections(cls):
        pass

    @classmethod
    def delete_selected(cls):
        pass

    @classmethod
    def move_selected(cls, x: float, y: float):
        pass

    def move(self, x: float, y: float):
        pass

    @classmethod
    def get_draft(cls):
        pass

    @classmethod
    def draw_map(cls, draw:ImageDraw.Draw, img_wh: int):
        pass
