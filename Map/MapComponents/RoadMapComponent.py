from Map.MapComponents.MapComponent import *
from functions.functions import hex_to_rgb
from Workspace.Drafts.LinesSequenceDraft import *
from svgwrite.shapes import Polyline as SVG_Polygon


class RoadMapComponent(MapComponent):
    _shape: LineString = None
    _base_shape: LineString = None
    _instances: List = []
    _draft: Type[LinesSequenceDraft] = LinesSequenceDraft
    _fill_ct_code = "bg"
    _mc_char: str = 'R'

    def __init__(self, workspace: IWorkspace, shape: LineString, map: IMap):
        super().__init__(workspace, shape, map)
        self._base_shape = shape
        self._shape = shape.buffer(20 / 320)
        self._objects_ids: List[int] = []
        self._joints_ids: List[int] = []
        for coord in range(0, len(shape.coords[:]) - 1):
            self._objects_ids.append(workspace.create_line(shape.coords[:][coord][0], shape.coords[:][coord][1],
                                                           shape.coords[:][coord + 1][0], shape.coords[:][coord + 1][1],
                                                           fill="#000000",
                                                           width=2 * int(self._is_selected), tags=type(self).__name__))
        for coord in shape.coords[:]:
            self._joints_ids.append(workspace.create_oval(coord[0] - 1, coord[1] - 1, coord[0] + 1, coord[1] + 1,
                                                          fill="#000000", tags=type(self).__name__, width=0))

        self.update_instance_ct()
        self.update_instance()

    def update_instance_ct(self):
        if self._is_selected:
            for coord in range(0, len(self._base_shape.coords[:]) - 1):
                self._workspace.itemconfig(self._objects_ids[coord], fill='#000')
            for joint in self._joints_ids:
                self._workspace.itemconfig(joint, fill='#000')
        else:
            for coord in range(0, len(self._base_shape.coords[:]) - 1):
                self._workspace.itemconfig(self._objects_ids[coord], fill=self._map.get_ct_field('cs'))
            for joint in self._joints_ids:
                self._workspace.itemconfig(joint, fill=self._map.get_ct_field('cs'))

    def update_instance(self):
        for coord in range(0, len(self._base_shape.coords[:]) - 1):
            self._workspace.coords(self._objects_ids[coord],
                                   self._workspace.calc_x(self._base_shape.coords[:][coord][0]),
                                   self._workspace.calc_y(self._base_shape.coords[:][coord][1]),
                                   self._workspace.calc_x(self._base_shape.coords[:][coord + 1][0]),
                                   self._workspace.calc_y(self._base_shape.coords[:][coord + 1][1]),
                                   )
        for coord in range(0, len(self._base_shape.coords[:])):
            self._workspace.coords(self._joints_ids[coord],
                                   self._workspace.calc_x(self._base_shape.coords[:][coord][0] - 20 / 320),
                                   self._workspace.calc_y(self._base_shape.coords[:][coord][1] - 20 / 320),
                                   self._workspace.calc_x(self._base_shape.coords[:][coord][0] + 20 / 320),
                                   self._workspace.calc_y(self._base_shape.coords[:][coord][1] + 20 / 320),
                                   )

        self.update_instance_scale()

    def update_instance_scale(self):
        for coord in range(0, len(self._base_shape.coords[:]) - 1):
            self._workspace.itemconfig(self._objects_ids[coord], width=(self._workspace.get_zoom() * 40 / 320))

    def move(self, x: float, y: float):
        def new_coords(coords: tuple):
            return [coords[0] + x, coords[1] + y]

        self._base_shape = LineString(list(map(new_coords, self._base_shape.coords[:])))
        self._shape = self._base_shape.buffer(20 / 320)
        self.update_instance()

    def draw_map_instance_image_draw(self, draw: ImageDraw.Draw, img_wh: int):
        map_wh = self._map.get_wh()

        def f(val):
            return round(val[0] / map_wh * img_wh), round(val[1] / map_wh * img_wh)

        draw.line(list(map(f, self._base_shape.coords[:])),
                  fill=hex_to_rgb(self._map.get_ct_field(self._fill_ct_code)), width=round(40 / 320 / map_wh * img_wh))

    def draw_map_instance_svgwrite(self, draw: Drawing, img_wh: int):
        map_wh = self._map.get_wh()

        def f(val):
            return (val[0] / map_wh * img_wh), (val[1] / map_wh * img_wh)

        poly = draw.add(SVG_Polygon(list(map(f, self._base_shape.coords[:]))))
        poly.stroke(self._map.get_ct_field('cs'), width=40 / 320 / map_wh * img_wh)
        poly.fill('none')

    def get_as_list(self) -> List:
        return list(map(list, self._base_shape.coords[:]))

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/road.png")

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map: IMap):
        try:
            list_of_polys = data['R']
            for _ in list_of_polys:
                cls.new_component(workspace, LineString(_), map)
        except KeyError:
            pass

    def lift_instance(self):
        for id in self._objects_ids:
            self._workspace.lift(id)
        for id in self._joints_ids:
            self._workspace.lift(id)

    def delete(self):
        super().delete()
        for id in self._objects_ids:
            self._workspace.delete(id)
        for id in self._joints_ids:
            self._workspace.delete(id)
