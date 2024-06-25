from Map.MapComponents.MapComponent import *


class PolyMapComponent(MapComponent):

    def __init__(self, map: Map, workspace: Workspace, shape: Polygon):
        super().__init__(map, workspace, shape)
        self.__object_id = workspace.create_polygon(shape.exterior.coords, outline="#000000", width=1, tags=self.__name__)

    def update_instance(self):
        self.__workspace.coords()

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/empty.png")
