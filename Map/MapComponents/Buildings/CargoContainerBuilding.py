from Map.MapComponents.Buildings.BaseBuilding import BaseBuilding
from GUI.IWorkspace import IWorkspace
from typing import Dict, Tuple
from Map.IMap import IMap
from shapely.geometry import Polygon
import math


class CargoContainerBuilding(BaseBuilding):
    type_id: int = 1
    _map_ct: str = 'w0'

    def __init__(self, workspace: IWorkspace, x: float, y: float, w: float, h: float, direction: int,pi:int, map: IMap):
        super().__init__(workspace, x, y, w, h,direction,pi, map)
        self._map.get_ct_field('e0')
        self._map.get_ct_field('w1')
        self._map.get_ct_field('e1')
        self._map.get_ct_field('w2')
        self._map.get_ct_field('e2')

    def set_w(self, val: float):
        self._w = 0.1

    def set_h(self, val: float):
        self._w = 0.05


