from tkinter import *
from GUI.IWorkspace import *
from shapely.geometry import *
from shapely.geometry import base
from Map.IMap import *
from Map.MapComponents.IMapComponent import *
from Workspace.Drafts.Draft import *
import keyboard
import logging
from svgwrite import Drawing


class MapComponent(IMapComponent):
    _workspace: IWorkspace = None
    _object_id: int = None
    _instances: List = []
    _shape: base.BaseGeometry = None
    _map: IMap = None
    _selected_instances: set = set()
    _is_selected: bool = False
    _draft: Type[Draft] = Draft
    _mc_char: str = ''
    _is_hidden: bool = False

    def __init__(self, workspace: IWorkspace, shape: base.BaseGeometry, map: IMap):
        self._workspace = workspace
        self._shape = shape
        self._map = map
        self._were_visible_on_screen = False
        self._is_instance_hidden = False

    def delete(self):
        try:
            self._workspace.delete(self._object_id)
            self._instances.remove(self)
        except:
            logging.exception('')

    def update_instance_ct(self):
        pass

    def update_visibility(self):
        if self._is_instance_hidden != self._is_hidden:
            self._is_instance_hidden = self._is_hidden
            if self._is_instance_hidden:
                self._workspace.itemconfig(self._object_id, state='hidden')
            else:
                self._workspace.itemconfig(self._object_id, state='normal')

    @classmethod
    def change_visibility(cls, val: bool):
        cls._is_hidden = val

    @classmethod
    def update_ct(cls):
        for mc in cls._instances:
            mc.update_instance_ct()

    def get_bounds(self):
        return self._shape.bounds

    @classmethod
    def update(cls, x0: float = None, x1: float = None, y0: float = None, y1: float = None):

        for instance in cls._instances:
            try:
                X0, Y0, X1, Y1 = instance.get_bounds()
                if X1 > x0 and X0 < x1 and Y1 > y0 and Y0 < y1:
                    instance.update_visibility()
                    if not instance._is_instance_hidden: instance.update_instance()

                    instance._were_visible_on_screen = True
                elif instance._were_visible_on_screen:
                    instance.update_visibility()
                    instance.update_instance()

                    instance._were_visible_on_screen = False
            except:
                pass

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
            selected_instance.select(x, y)
            cls._selected_instances.add(selected_instance)

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

    def select(self, x: float, y: float):
        self._is_selected = True
        self.update_instance_ct()

    def unselect(self):
        self._is_selected = False
        self.update_instance_ct()

    @classmethod
    def remove_all_selections(cls):
        for instance in cls._selected_instances:
            instance.unselect()
        cls._selected_instances = set()

    @classmethod
    def delete_selected(cls):
        for instance in cls._selected_instances:
            instance.delete()
        cls._selected_instances = set()

    @classmethod
    def move_selected(cls, x: float, y: float):
        for instance in cls._selected_instances:
            instance.move(x, y)

    def move(self, x: float, y: float):
        pass

    @classmethod
    def get_draft(cls) -> Type[Draft]:
        return cls._draft

    def draw_map_instance_image_draw(self, draw: ImageDraw.Draw, img_wh: int):
        pass

    def draw_map_instance_svgwrite(self, draw: Drawing, img_wh: int):
        pass

    @classmethod
    def draw_map_image_draw(cls, draw: ImageDraw.Draw, img_wh: int):
        for instance in cls._instances:
            instance.draw_map_instance_image_draw(draw, img_wh)

    @classmethod
    def draw_map_svgwrite(cls, draw: Drawing, img_wh: int):
        for instance in cls._instances:
            instance.draw_map_instance_svgwrite(draw, img_wh)

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
