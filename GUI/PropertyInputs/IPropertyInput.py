from typing import Protocol, Callable


class IPropertyInput:
    def __init__(self, master, getter: Callable[[], str], setter: Callable[[str], None], **kwargs):
        pass