from Map.MapComponents.PolyMapComponent import *


class BeachMapComponent(PolyMapComponent):
    _instances: List = []

    def update_instance_ct(self):
        self._workspace.itemconfig(self._object_id, fill=self._map.get_ct_field('gf'),outline=self._map.get_ct_field('gs')*int(self._is_selected), width=2*int(self._is_selected))

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map:IMap):
        try:
            list_of_polys = data['G']
            for _ in list_of_polys:
                cls.new_component(workspace, Polygon(_),map)
        except KeyError:
            pass

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/grass.png")
