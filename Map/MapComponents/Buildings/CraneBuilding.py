from Map.MapComponents.Buildings.DirectedBuilding import DirectedBuilding
from GUI.IWorkspace import IWorkspace
from typing import Dict, Tuple
from Map.IMap import IMap
from shapely.geometry import Polygon
import math


class CraneBuilding(DirectedBuilding):
    type_id: int = 4
    _map_ct: str = 'c1'
    _len_dirmark: float = 0.1

    def __init__(self, workspace: IWorkspace, x: float, y: float, w: float, h: float, direction: int,pi:int, map: IMap):
        super().__init__(workspace, x, y, w, h,direction,pi, map)
        self._map.get_ct_field('c0')
        self._map.get_ct_field('c2')

    def set_w(self, val: float):
        self._w = 0.1

    def set_h(self, val: float):
        self._w = 0.1


