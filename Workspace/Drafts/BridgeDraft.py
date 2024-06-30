from Workspace.Drafts.Draft import *


class BridgeDraft(Draft):
    _coords: List[tuple] = None
    _start_id: int = None
    _end_id: int = None
    _cls: IMapComponent = None

    def __init__(self, map: IMap, workspace: IWorkspace, cls: IMapComponent, x: float, y: float):
        super().__init__(map, workspace, cls, x, y)
        self._coords = [(self._start_x, self._start_y)]
        self._start_id = workspace.create_oval([0,0,0,0], outline='red', width=1, fill='')
        self.update()

    def select_btn(self, x: float, y: float):
        self._coords.append((x,y))
        self.complete()

    def delete(self):
        self._workspace.delete(self._start_id)
        self._workspace.remove_draft()

    def complete(self):
        self._cls.new_component(self._workspace, LineString(self._coords), self._map)
        super().complete()

    def update(self):
        self._workspace.coords(self._start_id,
                               [self._workspace.calc_x(self._coords[0][0]) - 10, self._workspace.calc_y(self._coords[0][1]) - 10, self._workspace.calc_x(self._coords[0][0]) + 10, self._workspace.calc_y(self._coords[0][1]) + 10])

