from Workspace.Drafts.PolyDraft import PolyDraft
from shapely.geometry import LineString


class LinesSequenceDraft(PolyDraft):
    def complete(self):
        if len(self._coords) < 2:
            self.cancel()
            return
        self._cls.new_component(self._workspace, LineString(self._coords), self._map)
        self.delete()
        self._workspace.update_layers()
