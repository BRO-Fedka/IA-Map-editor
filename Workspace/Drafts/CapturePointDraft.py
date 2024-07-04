from Workspace.Drafts.Draft import *


class CapturePointDraft(Draft):
    _coords: tuple = None
    _start_id: int = None
    _end_id: int = None
    _cls: IMapComponent = None

    def __init__(self, map: IMap, workspace: IWorkspace, cls: IMapComponent, x: float, y: float):
        super().__init__(map, workspace, cls, x, y)

        self._coords = (x, y)

    def select_btn(self, x: float, y: float):
        self.complete()

    def delete(self):
        self._workspace.remove_draft()

    def complete(self):
        self._cls.new_component(self._workspace, Point(self._coords), self._map, d=0.5, char=self._cls.get_free_char())
        super().complete()

