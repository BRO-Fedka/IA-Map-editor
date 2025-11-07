import math
from Workspace.Drafts.SinglePointDraft import SinglePointDraft
from Map.MapComponents.MapComponent import *
import json
from GUI.PropertyInputs.TextLinePI import TextLinePI
from GUI.PropertyInputs.ColorPI import ColorPI
from GUI.PropertyInputs.ComboBoxPI import ComboBoxPI
from GUI.PropertyInputs.LabelPI import LabelPI
from GUI.PropertyInputs.DirectionPI import DirectionPI

spawn_points_amount = 0


class SpawnPointMapComponent(MapComponent):
    _instances: List = []
    _draft: Type[SinglePointDraft] = SinglePointDraft
    _selected_instances: List = []
    _mc_char: str = '$'

    def __init__(self, workspace: IWorkspace, shape: Point, map: IMap, **kwargs):
        global spawn_points_amount
        super().__init__(workspace, shape, map)
        self._vx = (1, 0)
        self._vy = (0, 1)
        if 'id' in kwargs:
            self._id = kwargs['id']
            spawn_points_amount = max(spawn_points_amount, self._id + 1)
        else:
            self._id = spawn_points_amount
            spawn_points_amount += 1
        self._name = 'Unnamed'
        if 'name' in kwargs:
            self._name = kwargs['name']
        self._team = 'N'
        if 'team' in kwargs:
            self._team = kwargs['team']
        self._base_shape = shape
        self._shape: Polygon = self._base_shape.buffer(0.025)
        self.__direction = 0
        if 'dir' in kwargs:
            self.__direction = int(kwargs['dir'])
        self.__color = '#fff'
        if 'color' in kwargs:
            self.__color = kwargs['color']
        self._direction_marker_id = workspace.create_line(0, 0, 0, 0, fill='#000', width=2,
                                                              tags=type(self).__name__)
        self._object_id = workspace.create_oval(0, 0, 0, 0,
                                                outline="#000", fill=self.__color, width=3, tags=type(self).__name__)

        self.update_instance()

    def set_direction(self, val: int):
        self.__direction = val
        self.update_shape()

    def get_direction(self) -> int:
        return self.__direction

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_team(self):
        return self._team

    def set_team(self, team):
        self._team = team

    def get_id(self):
        return self._id

    def set_color(self, val: str):
        self.__color = val
        self.update_instance_ct()

    def get_color(self) -> str:
        return self.__color

    def update_shape(self):
        self._shape = self._base_shape.buffer(0.05)
        self.update_instance()

    def update_instance(self):

        self._workspace.coords(self._object_id, self._workspace.calc_x(self._base_shape.x - 0.05),
                               self._workspace.calc_y(self._base_shape.y - 0.05),
                               self._workspace.calc_x(self._base_shape.x + 0.05),
                               self._workspace.calc_y(self._base_shape.y + 0.05))
        self._workspace.coords(self._direction_marker_id,
                               self._workspace.calc_x(self._base_shape.x),
                               self._workspace.calc_y(self._base_shape.y),
                               self._workspace.calc_x(self._base_shape.x+math.cos(self.__direction/180*math.pi)*0.075),
                               self._workspace.calc_y(self._base_shape.y+math.sin(self.__direction/180*math.pi)*0.075))
        self.update_instance_ct()

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/spawnpoint.png")

    @classmethod
    def new_component(cls, workspace: IWorkspace, shape: Point, map: IMap, **kwargs):
        new_component = cls(workspace, shape, map, **kwargs)
        cls._instances.append(new_component)

        return new_component

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map: IMap):
        try:
            sps = data['$']
            for _ in sps:
                cls.new_component(workspace, Point(_[1], _[2]), map, color=_[3], id=int(_[0]), name=_[4], team=_[5], dir=int(_[6]))
        except KeyError:
            pass

    def move(self, x: float, y: float):
        self._base_shape = Point(self._base_shape.x + x, self._base_shape.y + y)
        self.update_shape()
        self.update_instance()

    def update_instance_ct(self):
        if self._is_selected:
            self._workspace.itemconfig(self._object_id, fill=self.__color, outline ='#000')
            self._workspace.itemconfig(self._direction_marker_id,state='normal')
        else:
            self._workspace.itemconfig(self._object_id, fill=self.__color, outline=self.__color)
            self._workspace.itemconfig(self._direction_marker_id,state='hidden')

    def get_as_list(self) -> List:
        return [self.get_id(), round(self._base_shape.x, 2), round(self._base_shape.y, 2), self.get_color(), self.get_name(), self.get_team(), self.get_direction()]

    def get_properties(self) -> List[MCProperty]:
        return [
            # MCProperty(DirectionPI, self.set_direction, self.get_direction, {}, "Direction"),
            MCProperty(LabelPI, None, self.get_id, {}, "ID"),
            MCProperty(TextLinePI, self.set_name, self.get_name, {}, "Name"),
            MCProperty(ColorPI, self.set_color, self.get_color, {}, "Color"),
            MCProperty(ComboBoxPI, self.set_team, self.get_team, {'values': ['R', 'B']}, "Team"),
            MCProperty(DirectionPI, self.set_direction, self.get_direction, {}, "Direction")

            # MCProperty(ComboBoxPI, self.set_type, self.get_type, {"values": list(VEHICLES_SHAPES.keys())}, "Type"),

        ]

    def lift_instance(self):
        super().lift_instance()
        self._workspace.lift(self._direction_marker_id)

    def delete(self):
        self._workspace.delete(self._direction_marker_id)
        super().delete()
