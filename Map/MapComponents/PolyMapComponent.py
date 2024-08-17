from Map.MapComponents.MapComponent import *
from Workspace.Drafts.PolyDraft import *
from functions.functions import hex_to_rgb
from Workspace.Drafts.PolySquareDraft import PolySquareDraft
from Workspace.Drafts.PolyDraft import PolyDraft
from Workspace.Drafts.PolySquareGridOrientedDraft import PolySquareGridOrientedDraft
import keyboard


class PolyMapComponent(MapComponent):
    _shape: Polygon = None
    _instances: List = []
    _draft: Type[PolyDraft] = PolyDraft
    _fill_ct_code = "bg"

    def __init__(self, workspace: IWorkspace, shape: Polygon, map: IMap):
        super().__init__(workspace, shape, map)
        self._object_id = workspace.create_polygon(shape.exterior.coords[:], outline="#000000",
                                                   width=2 * int(self._is_selected), tags=type(self).__name__)
        self.update_instance_ct()
        self.update_instance()

    def update_instance(self):
        poly_cords = []
        for coord in self._shape.exterior.coords[:]:
            poly_cords.append(self._workspace.calc_x(coord[0]))
            poly_cords.append(self._workspace.calc_y(coord[1]))
        self._workspace.coords(self._object_id, poly_cords)

    def move(self, x: float, y: float):
        def new_coords(coords: tuple):
            return [coords[0] + x, coords[1] + y]

        self._shape = Polygon(list(map(new_coords, self._shape.exterior.coords[:])))
        self.update_instance()

    def draw_map_instance(self, draw: ImageDraw.Draw, img_wh: int):
        map_wh = self._map.get_wh()

        def f(val):
            return round(val[0] / map_wh * img_wh), round(val[1] / map_wh * img_wh)

        draw.polygon(list(map(f, self._shape.exterior.coords[:])),
                     fill=hex_to_rgb(self._map.get_ct_field(self._fill_ct_code)))

    def get_as_list(self) -> List:
        return list(map(list, self._shape.exterior.coords[:]))

    @classmethod
    def get_draft(cls) -> Type[Draft]:
        if keyboard.is_pressed('shift'):
            return PolySquareDraft
        elif keyboard.is_pressed('ctrl'):
            return PolySquareGridOrientedDraft
        else:
            return PolyDraft
