from Map.MapComponents.PolyMapComponent import *


class BeachMapComponent(PolyMapComponent):

    def update_instance_ct(self):
        print(self._map.get_ct_field('bf'))
        self._workspace.itemconfig(self._object_id, fill=self._map.get_ct_field('bf'))

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map:IMap):
        try:
            list_of_polys = data['B']
            for _ in list_of_polys:
                cls.new_component(workspace, Polygon(_),map)
        except KeyError:
            pass

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/beach.png")
