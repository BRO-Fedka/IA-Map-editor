from Map.MapComponents.PolyMapComponent import *
from typing import *
from Map.IMap import *
from functions.functions import *
import json


class Map(IMap):
    __workspace: Workspace = None
    __data: Dict = {}
    __available_map_components: List[Type[MapComponent]]

    def __init__(self, data: dict, workspace: Workspace):
        self.__data = data
        self.__available_map_components = get_finite_inherits(MapComponent)
        print(self.__available_map_components)
        for mc in self.__available_map_components:
            mc.parse_map_raw_data_create_all(data,workspace)

    def update(self):
        for mc in self.__available_map_components:
            mc.update()

    @classmethod
    def from_json_file(cls, fp: str, workspace: Workspace):
        with open(fp) as file:
            parsed_json = json.load(file)
        new_map = Map(parsed_json, workspace)
        return new_map
