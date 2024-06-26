from typing import *
from Map.IMap import *
from functions.functions import *
import json
from Map.MapComponents.MapComponent import *
from Map.MapComponents.PolyMapComponent import *
from Map.MapComponents.BeachMapComponent import *
from Map.MapComponents.StoneMapComponent import *


class Map(IMap):
    __workspace: IWorkspace = None
    __data: Dict = {}
    __available_map_components: List[Type[MapComponent]]
    __ct: Dict[str,str] = None
    __wh: int = None

    def __init__(self, data: dict, workspace: IWorkspace):
        self.__data = data
        self.__available_map_components = get_finite_inherits(MapComponent)
        self.__ct = data['CT']
        self.__wh = data['WH']
        for mc in self.__available_map_components:
            mc.parse_map_raw_data_create_all(data,workspace, self)
        self.update_ct()

    def update_layer_sequence(self):
        for mc in self.__available_map_components:
            mc.lift()

    def update_ct(self):
        for mc in self.__available_map_components:
            mc.update_ct()

    def update(self):
        for mc in self.__available_map_components:
            mc.update()

    def get_ct_field(self,key:str) -> str:
        return self.__ct[key]

    def get_wh(self) -> int:
        return self.__wh

    @classmethod
    def from_json_file(cls, fp: str, workspace: IWorkspace):
        with open(fp) as file:
            parsed_json = json.load(file)
        new_map = Map(parsed_json, workspace)
        return new_map
