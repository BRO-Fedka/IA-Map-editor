import math

from Map.MapComponents.MapComponent import *
from Workspace.Drafts.PolyDraft import *
from functions.functions import hex_to_rgb
from Workspace.Drafts.PolySquareDraft import PolySquareDraft
from Workspace.Drafts.PolyDraft import PolyDraft
from Workspace.Drafts.PolySquareGridOrientedDraft import PolySquareGridOrientedDraft
import keyboard
from svgwrite.shapes import Polygon as SVG_Polygon


class PolyMapComponent(MapComponent):
    _shape: Polygon = None
    _instances: List = []
    _draft: Type[PolyDraft] = PolyDraft
    _fill_ct_code = "bg"

    def __init__(self, workspace: IWorkspace, shape: Polygon, map: IMap):
        super().__init__(workspace, shape, map)
        self._object_id = workspace.create_polygon(shape.exterior.coords[:], outline="#000000",
                                                   width=2 * int(self._is_selected), tags=type(self).__name__)
        self._selected_coords: Set[int] = set()
        self._selected_coords_ids: List[int] = []
        for coord in shape.exterior.coords[:]:
            self._selected_coords_ids.append(
                workspace.create_oval(coord[0] - 5, coord[1] - 5, coord[0] + 5, coord[1] + 5, fill='red', tags='markers', state='hidden'))
        self.update_instance_ct()
        self.update_instance()

    def update_instance_ct(self):
        for coord in range(0, len(self._shape.exterior.coords[:])):
            if coord in self._selected_coords:
                self._workspace.itemconfig(self._selected_coords_ids[coord],state='normal')
            else:
                self._workspace.itemconfig(self._selected_coords_ids[coord],state='hidden')

    def update_instance(self):
        poly_cords = []
        for coord in range(0, len(self._shape.exterior.coords[:])):
            poly_cords.append(self._workspace.calc_x(self._shape.exterior.coords[:][coord][0]))
            poly_cords.append(self._workspace.calc_y(self._shape.exterior.coords[:][coord][1]))
            self._workspace.coords(self._selected_coords_ids[coord],
                                   self._workspace.calc_x(self._shape.exterior.coords[:][coord][0])-5,
                                   self._workspace.calc_y(self._shape.exterior.coords[:][coord][1])-5,
                                   self._workspace.calc_x(self._shape.exterior.coords[:][coord][0])+5,
                                   self._workspace.calc_y(self._shape.exterior.coords[:][coord][1])+5
                                   )
        self._workspace.coords(self._object_id, poly_cords)

    def move(self, x: float, y: float):
        if len(self._selected_coords) == 0:
            def new_coords(coords: tuple):
                return [coords[0] + x, coords[1] + y]

            self._shape = Polygon(list(map(new_coords, self._shape.exterior.coords[:])))
            self.update_instance()
        else:
            n_coords = []
            for coord in range(0, len(self._shape.exterior.coords[:]) - 1):
                if coord in self._selected_coords:
                    n_coords.append([self._shape.exterior.coords[:][coord][0] + x / len(self._selected_coords),
                                     self._shape.exterior.coords[:][coord][1] + y / len(self._selected_coords)])
                else:
                    n_coords.append(
                        [self._shape.exterior.coords[:][coord][0], self._shape.exterior.coords[:][coord][1]])
            self._shape = Polygon(n_coords)
            self.update_instance()

    def draw_map_instance_image_draw(self, draw: ImageDraw.Draw, img_wh: int):
        map_wh = self._map.get_wh()

        def f(val):
            return round(val[0] / map_wh * img_wh), round(val[1] / map_wh * img_wh)

        draw.polygon(list(map(f, self._shape.exterior.coords[:])),
                     fill=hex_to_rgb(self._map.get_ct_field(self._fill_ct_code)))

    def draw_map_instance_svgwrite(self, draw: Drawing, img_wh: int):
        map_wh = self._map.get_wh()

        def f(val):
            return (val[0] / map_wh * img_wh), (val[1] / map_wh * img_wh)

        poly = draw.add(SVG_Polygon(list(map(f, self._shape.exterior.coords[:]))))
        poly.fill(self._map.get_ct_field(self._fill_ct_code))

    def get_as_list(self) -> List:
        return list(map(lambda v: list(map(lambda g: round(g,2),v)), self._shape.exterior.coords[:]))

    @classmethod
    def get_draft(cls) -> Type[Draft]:
        if keyboard.is_pressed('shift'):
            return PolySquareDraft
        elif keyboard.is_pressed('ctrl'):
            return PolySquareGridOrientedDraft
        else:
            return PolyDraft

    def select(self, x: float, y: float):
        if not keyboard.is_pressed('shift'):
            self._selected_coords = set()

        for coord in range(0, len(self._shape.exterior.coords[:]) - 1):
            if math.sqrt((self._shape.exterior.coords[:][coord][0] - x) ** 2 + (
                    self._shape.exterior.coords[:][coord][1] - y) ** 2) < 10 / self._workspace.get_zoom():
                self._selected_coords.add(coord)
        if len(self._selected_coords) > 0 or Point(x,y).intersects(self._shape):
            super().select(x, y)

    def unselect(self):
        self._selected_coords = set()
        super().unselect()

    def intersects(self, shape: base.BaseGeometry) -> bool:
        return self._shape.buffer(10 / self._workspace.get_zoom()).intersects(shape)

    def delete(self):
        for index in self._selected_coords_ids:
            self._workspace.delete(index)
        super().delete()
