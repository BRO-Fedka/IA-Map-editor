from Map.MapComponents.MapComponent import *
from functions.functions import hex_to_rgb, get_finite_inherits
from Workspace.Drafts.MultiPointDraft import *
from svgwrite.shapes import Polyline as SVG_Polygon
import math
from GUI.PropertyInputs.PositiveFloatPI import PositiveFloatPI
from GUI.PropertyInputs.DirectionPI import DirectionPI
from GUI.PropertyInputs.ButtonPI import ButtonPI
from GUI.PropertyInputs.ComboBoxPI import ComboBoxPI
from Map.MapComponents.Buildings.BaseBuilding import BaseBuilding
from Map.MapComponents.Buildings.HouseBuilding import HouseBuilding
from Map.MapComponents.Buildings.CargoContainerBuilding import CargoContainerBuilding
from Map.MapComponents.Buildings.HangarBuilding import HangarBuilding
from Map.MapComponents.Buildings.ChimneyBuilding import ChimneyBuilding
from Map.MapComponents.Buildings.CraneBuilding import CraneBuilding

lst = get_finite_inherits(BaseBuilding)
TREES_VARIANTS: Dict[str, Type[BaseBuilding]] = {}
TREES_TYPE_ID: Dict[int, Type[BaseBuilding]] = {}
for tree in lst:
    TREES_VARIANTS[tree.__name__] = tree
    TREES_TYPE_ID[tree.type_id] = tree


class BuildingsMapComponent(MapComponent):
    _shape: MultiPolygon = None
    _base_shape: MultiPoint = None
    _instances: List = []
    _draft: Type[MultiPointDraft] = MultiPointDraft
    _mc_char: str = '#'

    def __init__(self, workspace: IWorkspace, shape: MultiPoint, map: IMap):
        super().__init__(workspace, shape, map)
        self._base_shape = shape
        self._shape = shape.buffer(20 / 320)
        self._selected_trees: Set[int] = set()
        self._trees: List[BaseBuilding] = []
        for coord in shape.geoms:
            self._trees.append(HouseBuilding(workspace, coord.x, coord.y, 0.1, 0.1, 0, map))

        self.update_instance_ct()
        self.update_instance()
        self.update_shape()

    def update_visibility(self):
        if self._is_instance_hidden != self._is_hidden:
            self._is_instance_hidden = self._is_hidden
            for tree in self._trees:
                if self._is_instance_hidden:
                    tree.hide()
                else:
                    tree.show()

    def update_shape(self):
        n_coords: List[Polygon] = []
        for tree in self._trees:
            n_coords.append(tree.get_polygon())
        self._shape = MultiPolygon(n_coords)

    def update_instance_ct(self):
        for tree in self._trees:
            tree.update_ct()

    def update_instance(self):
        for tree in self._trees:
            tree.update()

        self.update_instance_scale()

    def update_instance_scale(self):
        for tree in self._trees:
            tree.update_scale()

    def move(self, x: float, y: float):

        if len(self._selected_trees) == 0:
            for tree in self._trees:
                tree.move(x, y)
        else:
            for tree_id in list(self._selected_trees):
                self._trees[tree_id].move(x, y)
        self.update_shape()
        self.update_instance()

    def draw_map_instance_image_draw(self, draw: ImageDraw.Draw, img_wh: int):
        for tree in self._trees:
            tree.draw_map_instance_image_draw(draw, img_wh)

    def draw_map_instance_svgwrite(self, draw: Drawing, img_wh: int):
        for tree in self._trees:
            tree.draw_map_instance_svgwrite(draw, img_wh)

    def get_as_list(self) -> List:
        def f(tree):
            return tree.get_as_list()

        return list(map(f, self._trees))

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/buildings.png")

    def add_tree(self, tree: BaseBuilding):
        self._trees.append(tree)

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map: IMap):
        try:
            list_of_trees = data['#']
            for tree_lst in list_of_trees:
                tcls = cls.new_component(workspace, MultiPoint(), map)
                for t in tree_lst:
                    try:
                        tcls.add_tree(TREES_TYPE_ID[t[0]](workspace, t[1], t[2], t[3], t[4], t[5], map))
                    except:pass
                tcls.update_shape()
                tcls.update_instance()
                tcls.update_ct()
                tcls.lift_instance()
        except KeyError:
            pass

    def lift_instance(self):
        for tree_cls in TREES_VARIANTS.values():
            self._workspace.lift(tree_cls.__name__)

    def delete(self):

        if len(self._selected_trees) == 0:
            for tree in self._trees:
                tree.delete()
            super().delete()
        else:
            sel_ids = list(self._selected_trees)

            self._selected_trees = set()
            sel_ids.sort()
            sel_ids.reverse()
            for tree_id in sel_ids:
                self._trees[tree_id].delete()
                self._trees.pop(tree_id)
        if len(self._trees) == 0:
            super().delete()
        else:
            self.update_instance()

    def unselect(self):
        for coord in range(0, len(self._trees)):
            self._trees[coord].unselect()
        self._selected_trees = set()
        super().unselect()

    def select(self, x: float, y: float):
        if not keyboard.is_pressed('shift'):
            for coord in range(0, len(self._trees)):
                self._trees[coord].unselect()
            self._selected_trees = set()

        for coord in range(0, len(self._trees)):
            if math.sqrt((self._trees[coord].x - x) ** 2 + (self._trees[coord].y - y) ** 2) < 20 / 320:
                self._selected_trees.add(coord)
                self._trees[coord].select()
        if len(self._selected_trees) > 0 or Point(x, y).intersects(self._base_shape):
            super().select(x, y)

    def intersects(self, shape: base.BaseGeometry) -> bool:
        for tree in self._shape.geoms:
            if tree.intersects(shape):
                return True
        return False

    def set_direction(self, val: int):
        for tree_id in list(self._selected_trees):
            self._trees[tree_id].set_direction(val)
        self.update_shape()

    def set_w(self, val: float):
        for tree_id in list(self._selected_trees):
            self._trees[tree_id].set_w(val)
        self.update_shape()

    def set_h(self, val: float):
        for tree_id in list(self._selected_trees):
            self._trees[tree_id].set_h(val)
        self.update_shape()

    def select_all(self):
        for tree_id in range(0, len(self._trees)):
            self._trees[tree_id].select()
            self._selected_trees.add(tree_id)

    def set_type(self, val: str):
        cls = TREES_VARIANTS[val]
        # print(cls)
        for tree_id in list(self._selected_trees):
            self._trees[tree_id].delete()
            self._trees[tree_id] = cls(self._workspace, self._trees[tree_id].x, self._trees[tree_id].y, 0.1, 0.1, 0,
                                       self._map)
            # print(self._trees[tree_id])
            self._trees[tree_id].select()
        self.update_shape()

    def get_properties(self) -> List[MCProperty]:
        if len(self._selected_trees) > 0:
            return [
                MCProperty(DirectionPI, self.set_direction,
                           lambda: self._trees[list(self._selected_trees)[0]].get_direction(), {}, "Direction"),
                MCProperty(PositiveFloatPI, self.set_w, lambda: self._trees[list(self._selected_trees)[0]].get_w(), {},
                           'Width'),
                MCProperty(PositiveFloatPI, self.set_h, lambda: self._trees[list(self._selected_trees)[0]].get_h(), {},
                           "Height"),
                MCProperty(ButtonPI, lambda: None, lambda: None, {'text': 'Select All', 'command': self.select_all},
                           ''),
                MCProperty(ComboBoxPI, self.set_type, lambda: type(self._trees[list(self._selected_trees)[0]]).__name__,
                           {'values': list(TREES_VARIANTS.keys())}, "Type")
            ]

        else:
            return []
