from GUI.IWorkspace import *


class MapGrid:
    __workspace: IWorkspace = None
    __border_id: int = None
    __WH: int = 0
    __vertical_lines_ids: List[int] = []
    __horizontal_lines_ids: List[int] = []

    def __init__(self, workspace: IWorkspace):
        self.__workspace = workspace
        self.__border_id = workspace.create_rectangle(0, 0, 0, 0, outline='#888', width=2)

    def lift(self):
        self.__workspace.lift(self.__border_id)
        for obj_id in self.__vertical_lines_ids:
            self.__workspace.lift(obj_id)
        for obj_id in self.__horizontal_lines_ids:
            self.__workspace.lift(obj_id)

    def update(self):
        self.__workspace.coords(self.__border_id, self.__workspace.calc_x(0), self.__workspace.calc_y(0),
                                self.__workspace.calc_x(self.__WH), self.__workspace.calc_y(self.__WH))
        while len(self.__vertical_lines_ids) < self.__WH - 1:
            self.__vertical_lines_ids.append(self.__workspace.create_line(0, 0, 0, 0, fill="#888", width=1))
        while len(self.__horizontal_lines_ids) < self.__WH - 1:
            self.__horizontal_lines_ids.append(self.__workspace.create_line(0, 0, 0, 0, fill="#888", width=1))
        for i in range(0, len(self.__horizontal_lines_ids)):
            line_x = i + 1
            if i >= self.__WH:
                line_x = self.__WH
            self.__workspace.coords(self.__horizontal_lines_ids[i], self.__workspace.calc_x(line_x),
                                    self.__workspace.calc_y(0), self.__workspace.calc_x(line_x),
                                    self.__workspace.calc_y(self.__WH))
        for i in range(0, len(self.__vertical_lines_ids)):
            line_y = i + 1
            if i >= self.__WH:
                line_y = self.__WH
            self.__workspace.coords(self.__vertical_lines_ids[i], self.__workspace.calc_x(0),
                                    self.__workspace.calc_y(line_y), self.__workspace.calc_x(self.__WH),
                                    self.__workspace.calc_y(line_y))

    def set_wh(self, wh: int = 16):
        self.__WH = wh
        self.update()
