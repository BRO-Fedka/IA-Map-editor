from tkinter import *
from GUI.Workspace import *
from shapely.geometry import *
from shapely.geometry import base


class MapComponent:
    __workspace: Workspace = None
    __map: Map = None
    __object_id: int = None
    __instances: List = []
    __shape: base.BaseGeometry = None

    def __init__(self, map: Map, workspace: Workspace, shape: base.BaseGeometry):
        self.__workspace = workspace
        self.__map = map
        self.__shape = shape

    @classmethod
    def update(cls):
        for instance in cls.__instances:
            instance.update_instance()

    def update_instance(self):
        pass
    @classmethod
    def new_component(cls, map: Map, workspace: Workspace):
        new_component = cls(map, workspace)
        cls.__instances.append(new_component)

        return new_component

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/empty.png")
