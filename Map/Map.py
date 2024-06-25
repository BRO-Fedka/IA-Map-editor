from typing import *
import json


class Map:
    __data: Dict = {}

    def __init__(self, data: Dict):
        self.__data = data

    @classmethod
    def from_json_file(cls, fp: str):
        with open(fp) as file:
            parsed_json = json.load(file)
        new_map = Map(parsed_json)
        return new_map
