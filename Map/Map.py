from Map.MapComponents.PolyMapComponent import *
from typing import *
import json


class Map:
    __data: Dict = {}
    __available_map_components: List[Type[MapComponent]]

    def __init__(self, data: Dict):
        self.__data = data
        self.__available_map_components = get_finite_inherits(MapComponent)

    @classmethod
    def from_json_file(cls, fp: str):
        with open(fp) as file:
            parsed_json = json.load(file)
        new_map = Map(parsed_json)
        return new_map


def get_finite_inherits(cls):
    finite_inherits = []

    def f(_cls):
        subclasses = _cls.__subclasses__()
        if len(subclasses) == 0:
            finite_inherits.append(_cls)
        else:
            for sc in subclasses:
                f(sc)

    f(cls)
    return finite_inherits
