from tkinter import *
from GUI.Workspace import *
from shapely.geometry import *
from shapely.geometry import base
from Map.IMap import *


class MapComponent:
    _workspace: Workspace = None
    _object_id: int = None
    _instances: List = []
    _shape: base.BaseGeometry = None
    _map: IMap = None

    def __init__(self, workspace: Workspace, shape: base.BaseGeometry, map: IMap):
        self._workspace = workspace
        self._shape = shape
        self._map = map

    def update_instance_ct(self):
        pass

    @classmethod
    def update_ct(cls):
        print('!')
        for mc in cls._instances:
            mc.update_instance_ct()

    @classmethod
    def update(cls):
        for instance in cls._instances:
            instance.update_instance()

    def update_instance(self):
        pass

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: Workspace, map:IMap):
        raise NotImplementedError

    @classmethod
    def lift(cls):
        for mc in cls._instances:
            mc.lift_instance()

    def lift_instance(self):
        self._workspace.lift(self._object_id)

    @classmethod
    def new_component(cls, workspace: Workspace, shape: base.BaseGeometry,map: IMap):
        # print(dir(cls))
        new_component = cls(workspace, shape,map)
        cls._instances.append(new_component)

        return new_component

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/empty.png")

    @classmethod
    def get_card_name(cls) -> str:
        return cls.__name__
