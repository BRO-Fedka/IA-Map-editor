from Map.MapComponents.Trees.BaseTree import BaseTree
from GUI.IWorkspace import IWorkspace
from typing import Dict
from Map.IMap import IMap


class ClassicalTree(BaseTree):
    sizes_of_stages: Dict[int,float] = {
        0:0.1,
        1:0.15,
        2:0.2,
        3:0.25,
    }
    type_id: int = 0

    def __init__(self, workspace: IWorkspace, x: float, y: float, stage: int, map:IMap):
        self._object_id = workspace.create_oval(0, 0, 0, 0, fill="#fff", outline='',
                                                tags=type(self).__name__)
        super().__init__(workspace, x, y, stage, map)

    def update(self):
        self._workspace.coords(self._object_id, self._workspace.calc_x(self.x - self._size / 2),
                               self._workspace.calc_y(self.y - self._size / 2),
                               self._workspace.calc_x(self.x + self._size / 2),
                               self._workspace.calc_y(self.y + self._size / 2))

    def update_ct(self):
        self._workspace.itemconfig(self._object_id, fill=self._map.get_ct_field('tf'))

    def select(self):
        super().select()
        self._workspace.itemconfig(self._object_id, outline="#000")

    def unselect(self):
        super().unselect()
        self._workspace.itemconfig(self._object_id, outline="")

    def delete(self):
        # print(self)
        self._workspace.delete(self._object_id)
        super().delete()
