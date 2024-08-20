from typing import *
from GUI.IWorkspace import *


class IMap(Protocol):

    def update(self):
        pass

    def update_ct(self):
        pass

    def get_ct_field(self, key: str) -> str:
        pass

    def set_ct_field(self, key: str, val: str):
        pass

    def get_ct_copy(self) -> Dict[str, str]:
        pass

    def get_wh(self) -> int:
        pass

    def update_layer_sequence(self):
        pass

    def get_preview_image_draw(self, wh: Optional[int], blur: Optional[bool]):
        pass

    def close(self):
        pass

    def load_ct(self, fp: str):
        pass

    def save_ct(self, fp: str):
        pass

    def get_fp(self) -> str:
        pass
