from Workspace.Drafts.Draft import *


class SinglePointDraft(Draft):
    _coords: tuple = None
    _start_id: int = None
    _end_id: int = None
    _cls: IMapComponent = None

    @classmethod
    def new_draft(cls, map: IMap, workspace: IWorkspace, cl: IMapComponent, x: float, y: float) -> Any:
        a = cls(map, workspace, cl, x, y)
        return None

    def __init__(self, map: IMap, workspace: IWorkspace, cls: IMapComponent, x: float, y: float):
        super().__init__(map, workspace, cls, x, y)
        self._coords = (x, y)
        self.complete()

    def select_btn(self, x: float, y: float):
        pass

    def delete(self):
        pass

    def complete(self):
        # print('!')
        self._cls.new_component(self._workspace, Point(self._coords), self._map)
        super().complete()
