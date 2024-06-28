from Map.MapComponents.MapComponent import *


class BridgeMapComponent(MapComponent):
    _instances: List = []
    _border_id: int = None
    _selection_id: int = None
    _base_shape: LineString = None

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
                print([(_[0], _[1]), (_[2], _[3])])
                cls.new_component(workspace, LineString([(_[0], _[1]), (_[2], _[3])]), map)
        except KeyError:
            pass

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/bridge.png")


