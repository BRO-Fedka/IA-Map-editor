from tkinter import *
from GUI.Workspace import *
from shapely.geometry import *
from shapely.geometry import base


class MapComponent:
    _workspace: Workspace = None
    _object_id: int = None
    _instances: List = []
    _shape: base.BaseGeometry = None

    def __init__(self, workspace: Workspace, shape: base.BaseGeometry):
        self._workspace = workspace
        self._shape = shape

    @classmethod
    def update(cls):
        for instance in cls._instances:
            instance.update_instance()

    def update_instance(self):
        pass

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: Workspace):
        raise NotImplementedError

    @classmethod
    def new_component(cls, workspace: Workspace, shape: base.BaseGeometry):
        # print(dir(cls))
        new_component = cls(workspace, shape)
        cls._instances.append(new_component)

        return new_component

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/empty.png")

    @classmethod
    def get_card_name(cls) -> str:
        return cls.__name__
