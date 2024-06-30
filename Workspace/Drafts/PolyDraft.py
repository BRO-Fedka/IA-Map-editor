from Workspace.Drafts.Draft import *


class PolyDraft(Draft):
    _coords: List[tuple] = None
    _start_id: int = None
    _end_id: int = None

    def __init__(self, map: IMap, workspace: IWorkspace, cls: IMapComponent, x: float, y: float):
        super().__init__(map, workspace, cls, x, y)
        self._coords = [(self._start_x, self._start_y)]
        self._object_id = workspace.create_polygon(self._coords, outline='red', width=1, fill='')
        self._start_id = workspace.create_oval([self._coords[0], self._coords[0]], outline='red', width=1, fill='')
        self._end_id = workspace.create_oval([self._coords[-1], self._coords[-1]], outline='red', width=1, fill='')
        self.update()

    def delete(self):
        self._workspace.delete(self._object_id)
        self._workspace.delete(self._start_id)
        self._workspace.delete(self._end_id)
        self._workspace.remove_draft()

    def complete(self):
        if len(self._coords) < 3:
            self.cancel()
            return
        self._cls.new_component(self._workspace, Polygon(self._coords), self._map)
        self.delete()

    def cancel(self):
        self.delete()

    def interact_btn(self, x: float, y: float):
        self.complete()

    def select_btn(self, x: float, y: float):
        self._coords.append((x, y))
        self.update()

    def update(self):
        poly_cords = []
        for coord in self._coords:
            poly_cords.append(self._workspace.calc_x(coord[0]))
            poly_cords.append(self._workspace.calc_y(coord[1]))
        self._workspace.coords(self._object_id, poly_cords)
        self._workspace.coords(self._start_id,
                               [poly_cords[0] - 10, poly_cords[1] - 10, poly_cords[0] + 10, poly_cords[1] + 10])
        print([poly_cords[-2] - 10, poly_cords[-1] - 10, poly_cords[-2] + 10, poly_cords[-1] + 10])
        self._workspace.coords(self._end_id,
                               [poly_cords[-2] - 10, poly_cords[-1] - 10, poly_cords[-2] + 10, poly_cords[-1] + 10])
