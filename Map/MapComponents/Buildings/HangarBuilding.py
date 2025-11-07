from Map.MapComponents.Buildings.BaseBuilding import BaseBuilding
from GUI.IWorkspace import IWorkspace
from typing import Dict, Tuple
from Map.IMap import IMap
from shapely.geometry import Polygon
import math


class HangarBuilding(BaseBuilding):
    type_id: int = 3
    _map_ct: str = 'hf'

    def __init__(self, workspace: IWorkspace, x: float, y: float, w: float, h: float, direction: int,pi:int, map: IMap):
        super().__init__(workspace, x, y, w, h,direction,pi, map)
        self._map.get_ct_field('hs')



