from Map.MapComponents.PolyMapComponent import *


class StoneMapComponent(PolyMapComponent):

    def update_instance_ct(self):
        self._workspace.itemconfig(self._object_id, fill=self._map.get_ct_field('sf'))

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map:IMap):
        try:
            list_of_polys = data['S']
            for _ in list_of_polys:
                cls.new_component(workspace, Polygon(_),map)
        except KeyError:
            pass

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/stone.png")
