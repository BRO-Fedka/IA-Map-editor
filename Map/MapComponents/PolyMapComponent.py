from Map.MapComponents.MapComponent import *


class PolyMapComponent(MapComponent):
    _shape: Polygon = None
    _instances: List = []

    def __init__(self, workspace: IWorkspace, shape: Polygon, map: IMap):
        super().__init__(workspace, shape, map)
        self._object_id = workspace.create_polygon(shape.exterior.coords[:], outline="#000000",
                                                   width=2 * int(self._is_selected), tags=type(self).__name__)

    def update_instance(self):
        poly_cords = []
        for coord in self._shape.exterior.coords[:]:
            poly_cords.append(self._workspace.calc_x(coord[0]))
            poly_cords.append(self._workspace.calc_y(coord[1]))
        # print(self._shape.exterior.coords[:])
        # print(poly_cords)
        # print(self._workspace.coords(self._object_id))
        self._workspace.coords(self._object_id, poly_cords)

    def move(self, x: float, y: float):

        def new_coords(coords :tuple):
            return [coords[0]+x,coords[1]+y]

        self._shape = Polygon(list(map(new_coords,self._shape.exterior.coords[:])))
        self.update_instance()
