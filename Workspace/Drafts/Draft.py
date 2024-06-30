from shapely.geometry import *
from Map.IMap import *
from Map.MapComponents.IMapComponent import *
from GUI.IWorkspace import *


class Draft:
    _cls: IMapComponent = None
    _map: IMap = None
    _workspace: IWorkspace = None
    _object_id: int = None
    _start_x: float = None
    _start_y: float = None

    def __init__(self, map: IMap, workspace: IWorkspace, cls: IMapComponent, x: float, y: float):
        self._cls = cls
        self._map = map
        self._workspace = workspace
        self._start_x = x
        self._start_y = y

    def complete(self):
        self.delete()
        self._workspace.update_layers()

    def cancel(self):
        self.delete()

    def delete(self):
        pass

    def interact_btn(self,x:float,y:float):
        pass

    def select_btn(self,x:float,y:float):
        pass

    def update(self):
        pass

    def lift(self):
        self._workspace.lift(self._object_id)
