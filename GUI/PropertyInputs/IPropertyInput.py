from typing import Protocol, Callable, Dict


class IPropertyInput(Protocol):
    def __init__(self, master, getter: Callable, setter: Callable, **kwargs:Dict):
        pass
