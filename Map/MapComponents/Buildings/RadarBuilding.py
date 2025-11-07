from Map.MapComponents.Buildings.CircularBuilding import CircularBuilding
from GUI.IWorkspace import IWorkspace
from Map.IMap import IMap


class RadarBuilding(CircularBuilding):
    type_id: int = 5
    _map_ct: str = 'hf'
    _observe_radius: float = 6

    def __init__(self, workspace: IWorkspace, x: float, y: float, w: float, h: float, direction: int, pi: int,
                 map: IMap):
        self._observer_zone_id = workspace.create_arc(0, 0, 0, 0, fill="", outline='#fff', width=1,
                                                      tags=type(self).__name__,start=-15,extent=30)

        super().__init__(workspace, x, y, w, h, direction, pi, map)
        self._map.get_ct_field('hs')

    def set_d(self, val):
        self._w = 0.15
        self._h = 0.15
        self.update_shape()

    def update(self):
        super().update()
        # print(dir(self))
        self._workspace.coords(self._observer_zone_id, self._workspace.calc_x(self.x - self._observe_radius),
                               self._workspace.calc_y(self.y - self._observe_radius),
                               self._workspace.calc_x(self.x + self._observe_radius),
                               self._workspace.calc_y(self.y + self._observe_radius))
        self._workspace.itemconfig(self._observer_zone_id,start=self.get_direction()-15) #,extent=30

    def delete(self):
        super().delete()
        self._workspace.delete(self._observer_zone_id)
