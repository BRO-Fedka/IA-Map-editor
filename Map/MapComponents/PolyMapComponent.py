from Map.MapComponents.MapComponent import *
from Map.Map import *


class PolyMapComponent(MapComponent):
    def __init__(self, map: Map, workspace: Workspace):
        super().__init__(map, workspace)

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/empty.png")
