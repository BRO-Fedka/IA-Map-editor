import math
from Workspace.Drafts.SinglePointDraft import SinglePointDraft
from Map.MapComponents.MapComponent import *
import json
from GUI.PropertyInputs.DirectionPI import DirectionPI
from GUI.PropertyInputs.ColorPI import ColorPI
from GUI.PropertyInputs.ComboBoxPI import ComboBoxPI

with open('VehiclesShapes.json') as f:
    VEHICLES_SHAPES: Dict[str, List[Tuple[float, float]]] = json.load(f)


class VehicleDummyMapComponent(MapComponent):
    _instances: List = []
    _draft: Type[SinglePointDraft] = SinglePointDraft
    _selected_instances: List = []

    def _calc_xy(self, coords: Tuple[float, float]) -> Tuple[float, float]:
        return self._base_shape.x + coords[0] * self._vx[0] + coords[1] * self._vy[0], self._base_shape.y + coords[0] * \
               self._vx[1] + coords[1] * self._vy[1]

    def __init__(self, workspace: IWorkspace, shape: Point, map: IMap):
        super().__init__(workspace, shape, map)
        self._vx = (1, 0)
        self._vy = (0, 1)
        self._base_shape = shape
        self._shape: Polygon = Polygon()
        self.__type = list(VEHICLES_SHAPES.keys())[0]
        self.__direction = 0
        self.__color = "#888"
        self._poly_shape = VEHICLES_SHAPES[self.__type]
        self._object_id = workspace.create_polygon(self._poly_shape,
                                                   outline="#000", fill=self.__color, width=0, tags=type(self).__name__)
        self.set_direction(0)
        self.update_instance()

    def set_type(self, value: str):
        self.__type = value
        self._poly_shape = VEHICLES_SHAPES[value]
        self.update_shape()

    def get_type(self):
        return self.__type

    def set_direction(self, val: int):
        self.__direction = val
        self._vx = (math.cos(val / 180 * math.pi), math.sin(val / 180 * math.pi))
        self._vy = (-math.sin(val / 180 * math.pi), math.cos(val / 180 * math.pi))
        self.update_shape()

    def get_direction(self) -> int:
        return self.__direction

    def set_color(self, val: str):
        self.__color = val
        self.update_instance_ct()

    def get_color(self) -> str:
        return self.__color

    def update_shape(self):
        current_poly = list(map(self._calc_xy, self._poly_shape))
        self._shape = Polygon(current_poly)
        self.update_instance()

    def update_instance(self):
        poly_cords = []
        for coord in self._shape.exterior.coords[:]:
            poly_cords.append(self._workspace.calc_x(coord[0]))
            poly_cords.append(self._workspace.calc_y(coord[1]))
        self._workspace.coords(self._object_id, poly_cords)
        self.update_instance_ct()

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/vehicle.png")

    @classmethod
    def new_component(cls, workspace: IWorkspace, shape: Point, map: IMap, **kwargs):
        new_component = cls(workspace, shape, map, **kwargs)
        cls._instances.append(new_component)

        return new_component

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map: IMap):
        pass

    def move(self, x: float, y: float):
        self._base_shape = Point(self._base_shape.x + x, self._base_shape.y + y)
        self.update_shape()
        self.update_instance()

    def update_instance_ct(self):
        self._workspace.itemconfig(self._object_id,
                                   width=0 + 3 * int(self._is_selected), fill=self.__color)

    def get_properties(self) -> List[MCProperty]:
        return [
            MCProperty(DirectionPI, self.set_direction, self.get_direction, {}, "Direction"),
            MCProperty(ColorPI, self.set_color, self.get_color, {}, "Color"),
            MCProperty(ComboBoxPI, self.set_type, self.get_type, {"values": list(VEHICLES_SHAPES.keys())}, "Type"),

        ]
