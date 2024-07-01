from typing import *
from GUI.IWorkspace import *


class IMap(Protocol):

    def update(self):
        pass

    def update_ct(self):
        pass

    def get_ct_field(self, key: str) -> str:
        pass

    def get_wh(self) -> int:
        pass

    def update_layer_sequence(self):
        pass

    def get_preview_image_png(self, wh:Optional[int], blur:Optional[bool]):
        pass
