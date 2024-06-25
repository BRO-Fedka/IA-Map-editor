from Map.MapComponents.PolyMapComponent import *


class StoneMapComponent(PolyMapComponent):

    def __init__(self,  workspace: Workspace, shape: Polygon):
        super().__init__(workspace, shape)
        workspace.itemconfig(self._object_id, fill="#888888")

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: Workspace):
        try:
            list_of_polys = data['S']
            for _ in list_of_polys:
                cls.new_component(workspace, Polygon(_))
        except KeyError:
            pass
    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/stone.png")
