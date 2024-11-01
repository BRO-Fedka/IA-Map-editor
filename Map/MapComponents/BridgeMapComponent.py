import svgwrite.shapes

from Map.MapComponents.MapComponent import *
from Workspace.Drafts.SingeLineDraft import *
from functions.functions import hex_to_rgb
from svgwrite import Drawing


class BridgeMapComponent(MapComponent):
    _instances: List = []
    _border_id: int = None
    _selection_id: int = None
    _base_shape: LineString = None
    _draft: Type[SingeLineDraft] = SingeLineDraft
    _mc_char: str = '_'

    def __init__(self, workspace: IWorkspace, shape: LineString, map: IMap):
        super().__init__(workspace, shape, map)
        self._base_shape = shape
        self._shape = shape.buffer(60 / 320)
        self._selection_id = workspace.create_line((0, 0, 0, 0), fill="#000000",
                                                   width=1, tags=type(self).__name__)
        self._border_id = workspace.create_line((0, 0, 0, 0), fill="#000000",
                                                width=self._workspace.get_zoom() * 60 / 320, tags=type(self).__name__)
        self._object_id = workspace.create_line((0, 0, 0, 0), fill="#000000",
                                                width=self._workspace.get_zoom() * 50 / 320, tags=type(self).__name__)
        self.update_instance_ct()
        self.update_instance()

    def update_visibility(self):
        if self._is_instance_hidden != self._is_hidden:
            self._is_instance_hidden = self._is_hidden
            if self._is_instance_hidden:
                self._workspace.itemconfig(self._object_id,state='hidden')
                self._workspace.itemconfig(self._border_id,state='hidden')
                self._workspace.itemconfig(self._selection_id,state='hidden')
            else:
                self._workspace.itemconfig(self._object_id, state='normal')
                self._workspace.itemconfig(self._border_id, state='normal')
                self._workspace.itemconfig(self._selection_id, state='normal')

    def update_instance(self):
        self._workspace.coords(self._object_id, (
            self._workspace.calc_x(self._base_shape.coords[0][0]),
            self._workspace.calc_y(self._base_shape.coords[0][1]),
            self._workspace.calc_x(self._base_shape.coords[1][0]),
            self._workspace.calc_y(self._base_shape.coords[1][1])
        ))
        self._workspace.coords(self._border_id, (
            self._workspace.calc_x(self._base_shape.coords[0][0]),
            self._workspace.calc_y(self._base_shape.coords[0][1]),
            self._workspace.calc_x(self._base_shape.coords[1][0]),
            self._workspace.calc_y(self._base_shape.coords[1][1])
        ))
        self._workspace.coords(self._selection_id, (
            self._workspace.calc_x(self._base_shape.coords[0][0]),
            self._workspace.calc_y(self._base_shape.coords[0][1]),
            self._workspace.calc_x(self._base_shape.coords[1][0]),
            self._workspace.calc_y(self._base_shape.coords[1][1])
        ))
        self.update_instance_scale()

    def update_instance_scale(self):
        self._workspace.itemconfig(self._selection_id,
                                   width=self._workspace.get_zoom() * 60 / 320 + 4 * int(self._is_selected))
        self._workspace.itemconfig(self._border_id, width=self._workspace.get_zoom() * 60 / 320)
        self._workspace.itemconfig(self._object_id, width=self._workspace.get_zoom() * 50 / 320)

    def delete(self):
        super().delete()
        self._workspace.delete(self._border_id)
        self._workspace.delete(self._selection_id)

    def move(self, x: float, y: float):

        def new_coords(coords: tuple):
            return [coords[0] + x, coords[1] + y]

        self._base_shape = LineString(list(map(new_coords, self._base_shape.coords[:])))
        self._shape = self._base_shape.buffer(60 / 320)
        self.update_instance()

    def update_instance_ct(self):
        # outline="#000000" * int(self._is_selected)
        self._workspace.itemconfig(self._selection_id,
                                   width=self._workspace.get_zoom() * 60 / 320 + 4 * int(self._is_selected))
        self._workspace.itemconfig(self._object_id, fill=self._map.get_ct_field('b0'))
        self._workspace.itemconfig(self._border_id, fill=self._map.get_ct_field('b1'))

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map: IMap):
        try:
            list_of_polys = data['_']
            for _ in list_of_polys:
                cls.new_component(workspace, LineString([(_[0], _[1]), (_[2], _[3])]), map)
        except KeyError:
            pass

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/bridge.png")

    def lift_instance(self):
        self._workspace.lift(self._border_id)
        super().lift_instance()

    def draw_map_instance_image_draw(self, draw: ImageDraw.Draw, img_wh: int):
        map_wh = self._map.get_wh()

        def f(val):
            return round(val[0] / map_wh * img_wh), round(val[1] / map_wh * img_wh)

        draw.line(list(map(f, self._base_shape.coords[:])), fill=hex_to_rgb(self._map.get_ct_field('b0')),
                  width=round(60 / 320 / map_wh * img_wh))

    def draw_map_instance_svgwrite(self, draw: Drawing, img_wh: int):
        map_wh = self._map.get_wh()

        def f(val):
            return round(val[0] / map_wh * img_wh), round(val[1] / map_wh * img_wh)

        line = draw.add(svgwrite.shapes.Line(list(map(f, self._base_shape.coords[:]))[0],
                                             list(map(f, self._base_shape.coords[:]))[1], ))
        line.stroke(color=self._map.get_ct_field('b0'), width=60 / 320 / map_wh * img_wh)

    def get_as_list(self) -> List:
        return [round(self._base_shape.coords[0][0],2), round(self._base_shape.coords[0][1],2), round(self._base_shape.coords[1][0],2),
                round(self._base_shape.coords[1][1],2)]
