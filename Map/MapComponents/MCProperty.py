from typing import NamedTuple, Callable, Dict, Any, Type
from GUI.PropertyInputs.IPropertyInput import IPropertyInput


class MCProperty(NamedTuple):
    widget: Type[IPropertyInput]
    setter: Callable
    getter: Callable
    kwards: Dict[str, Any]
    name: str
