from Map.MapComponents.PolyMapComponent import *


class BeachMapComponent(PolyMapComponent):
    _instances: List = []
    _fill_ct_code = "bf"
    _mc_char: str = 'B'

    def __init__(self, workspace: IWorkspace, shape: Polygon, map: IMap):
        self._object_z0_id = workspace.create_polygon(shape.exterior.coords[:], outline="#000000", fill='',
                                                      width=2 * int(self._is_selected), tags='shore0')
        self._object_z1_id = workspace.create_polygon(shape.exterior.coords[:], outline="#000000", fill='',
                                                      width=2 * int(self._is_selected), tags='shore1')
        super().__init__(workspace, shape, map)

    def delete(self):
        self._workspace.delete(self._object_z1_id)
        self._workspace.delete(self._object_z0_id)
        super().delete()
        # self._instances.remove(self) ??????

    def update_instance_ct(self):
        if self._is_selected:
            self._workspace.itemconfig(self._object_id, fill=self._map.get_ct_field('bf'), outline="#000", width=2)
        else:
            self._workspace.itemconfig(self._object_id, fill=self._map.get_ct_field('bf'),
                                       outline=self._map.get_ct_field('bs'))
        self._workspace.itemconfig(self._object_z0_id,
                                   outline=self._map.get_ct_field('zs'))
        self._workspace.itemconfig(self._object_z1_id,
                                   outline=self._map.get_ct_field('zf'))

    def update_instance(self):
        super().update_instance()
        self._workspace.coords(self._object_z1_id, self._workspace.coords(self._object_id))
        self._workspace.coords(self._object_z0_id, self._workspace.coords(self._object_id))
        self.update_instance_scale()

    def update_instance_scale(self):
        self._workspace.itemconfig(self._object_id,
                                   width=(self._workspace.get_zoom() * 10 / 320) * int(not self._is_selected) + 2 * int(
                                       self._is_selected))
        self._workspace.itemconfig(self._object_z0_id, width=(self._workspace.get_zoom() * 160 / 320))
        self._workspace.itemconfig(self._object_z1_id, width=(self._workspace.get_zoom() * 80 / 320))


    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map: IMap):
        try:
            list_of_polys = data['B']
            for _ in list_of_polys:
                cls.new_component(workspace, Polygon(_), map)
        except KeyError:
            pass

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/beach.png")
