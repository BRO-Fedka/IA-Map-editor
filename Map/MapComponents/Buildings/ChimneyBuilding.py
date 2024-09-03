from Map.MapComponents.Buildings.BaseBuilding import BaseBuilding
from GUI.IWorkspace import IWorkspace
from typing import Dict, Tuple
from Map.IMap import IMap
from shapely.geometry import Polygon
import math


class ChimneyBuilding(BaseBuilding):
    type_id: int = 2
    _map_ct: str = 'if'

    def __init__(self, workspace: IWorkspace, x: float, y: float, w: float, h: float, direction: int, map: IMap):
        super().__init__(workspace, x, y, w, h,direction, map)
        self._map.get_ct_field('is')
        self._map.get_ct_field('io')

    def set_w(self, val: float):
        self._w = 0.1

    def set_h(self, val: float):
        self._w = 0.1


