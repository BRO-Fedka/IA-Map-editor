from typing import *


class IMap(Protocol):

    def update(self):
        pass

    def update_ct(self):
        pass

    def get_ct_field(self, key: str) -> str:
        pass

    def get_wh(self) -> int:
        pass
