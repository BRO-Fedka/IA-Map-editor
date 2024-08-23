from Map.MapComponents.Buildings.BaseBuilding import BaseBuilding
from GUI.IWorkspace import IWorkspace
from typing import Dict, Tuple
from Map.IMap import IMap
from shapely.geometry import Polygon
import math


class HouseBuilding(BaseBuilding):
    type_id: int = 0
    _map_ct: str = 'rr'

    def __init__(self, workspace: IWorkspace, x: float, y: float, w: float, h: float, direction: int, map: IMap):
        super().__init__(workspace, x, y, w, h,direction, map)
        self._map.get_ct_field('rl')

