from typing import *
from tkinter import *


class IField(Protocol):
    def get(self) -> str:
        pass

    def grid(self, **kwargs):
        pass
