from Map.MapComponents.MapComponent import *
from Workspace.Drafts.PolyDraft import *


class PolyMapComponent(MapComponent):
    _shape: Polygon = None
    _instances: List = []
    _draft: Type[PolyDraft] = PolyDraft

    def __init__(self, workspace: IWorkspace, shape: Polygon, map: IMap):
        print('!')
        super().__init__(workspace, shape, map)
        self._object_id = workspace.create_polygon(shape.exterior.coords[:], outline="#000000",
                                                   width=2 * int(self._is_selected), tags=type(self).__name__)
        self.update_instance_ct()
        self.update_instance()

    def update_instance(self):
        poly_cords = []
        for coord in self._shape.exterior.coords[:]:
            poly_cords.append(self._workspace.calc_x(coord[0]))
            poly_cords.append(self._workspace.calc_y(coord[1]))
        self._workspace.coords(self._object_id, poly_cords)

    def move(self, x: float, y: float):

        def new_coords(coords :tuple):
            return [coords[0]+x,coords[1]+y]

        self._shape = Polygon(list(map(new_coords,self._shape.exterior.coords[:])))
        self.update_instance()

