from tkinter import *
from GUI.IWorkspace import *
from shapely.geometry import *
from shapely.geometry import base
from Map.IMap import *
from Map.MapComponents.IMapComponent import *
from Workspace.Drafts.Draft import *
import keyboard
import logging


class MapComponent(IMapComponent):
    _workspace: IWorkspace = None
    _object_id: int = None
    _instances: List = []
    _shape: base.BaseGeometry = None
    _map: IMap = None
    _selected_instances = []
    _is_selected: bool = False
    _draft: Type[Draft] = Draft
    _mc_char: str = ''

    def __init__(self, workspace: IWorkspace, shape: base.BaseGeometry, map: IMap):
        self._workspace = workspace
        self._shape = shape
        self._map = map

    def delete(self):
        try:
            self._workspace.delete(self._object_id)
            self._instances.remove(self)
        except:
            logging.exception('')

    def update_instance_ct(self):
        pass

    @classmethod
    def update_ct(cls):
        for mc in cls._instances:
            mc.update_instance_ct()

    @classmethod
    def update(cls):
        for instance in cls._instances:
            instance.update_instance()

    def update_instance(self):
        pass

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map: IMap):
        raise NotImplementedError

    @classmethod
    def lift(cls):
        for mc in cls._instances:
            mc.lift_instance()

    def lift_instance(self):
        self._workspace.lift(self._object_id)

    @classmethod
    def new_component(cls, workspace: IWorkspace, shape: base.BaseGeometry, map: IMap, **kwargs):
        new_component = cls(workspace, shape, map)
        cls._instances.append(new_component)

        return new_component

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/empty.png")

    @classmethod
    def get_card_name(cls) -> str:
        return cls.__name__

    @classmethod
    def select_at_coords(cls, x: float, y: float):
        cursor_point = Point(x, y)
        selected_instance = None
        for instance in cls._instances:
            if instance.intersects(cursor_point):
                selected_instance = instance
        if not keyboard.is_pressed('shift'):
            cls.remove_all_selections()
        if not (selected_instance is None):
            selected_instance.select()
            cls._selected_instances.append(selected_instance)

    def intersects(self, shape: base.BaseGeometry) -> bool:
        return self._shape.intersects(shape)

    @classmethod
    def get_selected_instances(cls) -> List:
        lst = []
        for instance in cls._instances:
            if instance.is_selected():
                lst.append(instance)
        return lst

    def is_selected(self) -> bool:
        return self._is_selected

    def select(self):
        self._is_selected = True
        self.update_instance_ct()

    def unselect(self):
        self._is_selected = False
        self.update_instance_ct()

    @classmethod
    def remove_all_selections(cls):
        for instance in cls._selected_instances:
            instance.unselect()
        cls._selected_instances = []

    @classmethod
    def delete_selected(cls):
        for instance in cls._selected_instances:
            instance.delete()
        cls._selected_instances = []

    @classmethod
    def move_selected(cls, x: float, y: float):
        for instance in cls._selected_instances:
            instance.move(x, y)

    def move(self, x: float, y: float):
        pass

    @classmethod
    def get_draft(cls) -> Type[Draft]:
        return cls._draft

    def draw_map_instance(self, draw: ImageDraw.Draw, img_wh: int):
        pass

    @classmethod
    def draw_map(cls, draw: ImageDraw.Draw, img_wh: int):
        for instance in cls._instances:
            instance.draw_map_instance(draw, img_wh)

    @classmethod
    def delete_all(cls):
        for instance in cls._instances:
            instance.delete()
        cls._instances = []

    @classmethod
    def fill_q(cls, q: Dict[tuple, Dict[str, List[int]]], q_col: Dict[tuple, base.BaseGeometry], wh: int):
        for x in range(0, wh):
            for y in range(0, wh):
                col = q_col[(x, y)]
                q[x][y][cls._mc_char] = []
                for instance_id in range(0, len(cls._instances)):
                    if cls._instances[instance_id].intersects(col):
                        q[x][y][cls._mc_char].append(instance_id)

    @classmethod
    def fill_data(cls, map_data: Dict):
        map_data[cls._mc_char] = []
        for instance in cls._instances:
            map_data[cls._mc_char].append(instance.get_as_list())

    def get_as_list(self) -> List:
        return []

    def get_properties(self) -> List[MCProperty]:
        return []
