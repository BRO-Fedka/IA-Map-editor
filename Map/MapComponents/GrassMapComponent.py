from Map.MapComponents.PolyMapComponent import *


class BeachMapComponent(PolyMapComponent):
    _instances: List = []
    _fill_ct_code = "gf"

    def update_instance_ct(self):
        if self._is_selected:
            self._workspace.itemconfig(self._object_id, fill=self._map.get_ct_field('gf'), outline="#000", width=2)
        else:
            self._workspace.itemconfig(self._object_id, fill=self._map.get_ct_field('gf'),
                                       outline=self._map.get_ct_field('gs'))

    def update_instance(self):
        super().update_instance()
        self.update_instance_scale()

    def update_instance_scale(self):
        self._workspace.itemconfig(self._object_id,width=(self._workspace.get_zoom() * 10 / 320)*int(not self._is_selected)+ 2*int(self._is_selected))

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map: IMap):
        try:
            list_of_polys = data['G']
            for _ in list_of_polys:
                cls.new_component(workspace, Polygon(_), map)
        except KeyError:
            pass

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/grass.png")
