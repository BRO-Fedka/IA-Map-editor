from Map.MapComponents.IMapComponent import *


class IMapComponentCard(Protocol):

    def __init__(self, master: Optional[Misc], map_component: Type[IMapComponent], **kwargs):
        pass

    def is_selected(self) -> bool:
        pass

    def select(self):
        pass

    def unselect(self):
        pass

    def get_map_component(self) -> Type[IMapComponent]:
        pass
