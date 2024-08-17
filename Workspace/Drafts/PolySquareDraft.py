from Workspace.Drafts.PolyDraft import PolyDraft
from typing import List, Tuple
from Map.IMap import IMap
from GUI.IWorkspace import IWorkspace
from Map.MapComponents.IMapComponent import IMapComponent
from shapely.geometry import Polygon
import math


class PolySquareDraft(PolyDraft):
    _coords: List[Tuple[float, float]] = None
    _start_id: int = None
    _end_id: int = None
    axises_base_vectors: Tuple[Tuple[float, float]] = None
    axis_base_vector_length: float = None

    def select_btn(self, x: float, y: float):
        if len(self._coords) > 1:
            vec1 = (x - self._coords[len(self._coords) - 1][0], y - self._coords[len(self._coords) - 1][1])
            length = math.sqrt(vec1[0] ** 2 + vec1[1] ** 2)
            for vec0 in self.axises_base_vectors:
                cos = (vec0[0] * vec1[0] + vec0[1] * vec1[1]) / self.axis_base_vector_length / length
                if cos >= (1 / math.sqrt(2)):
                    x = self._coords[len(self._coords) - 1][0] + vec0[0] / self.axis_base_vector_length * length * cos
                    y = self._coords[len(self._coords) - 1][1] + vec0[1] / self.axis_base_vector_length * length * cos
        self._coords.append((x, y))
        if len(self._coords) == 2:
            x, y = self._coords[1][0] - self._coords[0][0], self._coords[1][1] - self._coords[0][1]
            self.axises_base_vectors = tuple([(x, y), (y, -x), (-x, -y), (-y, x)])
            self.axis_base_vector_length = math.sqrt(x ** 2 + y ** 2)
        self.update()
