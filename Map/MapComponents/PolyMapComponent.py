from Map.MapComponents.MapComponent import *


class PolyMapComponent(MapComponent):
    _shape: Polygon = None

    def __init__(self, workspace: Workspace, shape: Polygon):
        super().__init__(workspace, shape)
        # print(shape.exterior.coords[:])
        self._object_id = workspace.create_polygon(shape.exterior.coords[:], outline="#000000", width=1, tags=type(self).__name__)

    def update_instance(self):
        poly_cords = []
        for coord in self._shape.exterior.coords[:]:
            poly_cords.append(self._workspace.calc_x(coord[0]))
            poly_cords.append(self._workspace.calc_y(coord[1]))
        # print(self._shape.exterior.coords[:])
        # print(poly_cords)
        # print(self._workspace.coords(self._object_id))
        self._workspace.coords(self._object_id, poly_cords)
