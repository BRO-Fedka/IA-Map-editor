from tkinter import *
from typing import *
from Map.IMap import IMap


class Workspace(Canvas):
    __map: IMap = None
    __zoom: float = 320
    __view_center_x: float = 0
    __view_center_y: float = 0
    __prev_cursor_x: float = 0
    __prev_cursor_y: float = 0
    __is_cursor_held: bool = False
    __held_button: int = 0

    def __init__(self, master: Optional[Misc], **kwargs):
        super().__init__(master, kwargs)
        self['highlightthickness'] = 0
        self['cursor'] = 'crosshair'
        self.__grid: MapGrid = MapGrid(self)
        self.__grid.set_wh(16)
        self.update_content()
        self.bind('<MouseWheel>', self.__on_wheel)
        self.bind('<Configure>', self.__on_configure)
        self.bind('<Motion>', self.__on_motion)
        self.bind("<ButtonPress>", self.__on_press)
        self.bind("<ButtonRelease>", self.__on_release)

    def set_map(self, map: IMap):
        self.__map = map
        self.update_map()
        self.__grid.lift()

    def update_map(self):
        if self.__map is None:
            pass
        else:
            self.__map.update()

    def update_content(self):
        self.__grid.update()
        self.update_map()

    def calc_x(self, x: float):
        return (x - self.__view_center_x) * self.__zoom + self.winfo_width() / 2

    def calc_y(self, y: float):
        return (y - self.__view_center_y) * self.__zoom + self.winfo_height() / 2

    def set_zoom(self, zoom: float):
        if zoom < 10:
            zoom = 10
        elif zoom > 1000:
            zoom = 1000
        self.__zoom = zoom
        self.update_content()

    def zoom_in(self):
        self.set_zoom(self.__zoom * 1.1)

    def zoom_out(self):
        self.set_zoom(self.__zoom / 1.1)

    def get_zoom(self):
        return self.__zoom

    def __on_wheel(self, event):
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()

    def __on_configure(self, event):
        self.update_content()

    def __on_motion(self, event):
        if self.__is_cursor_held:
            if self.__held_button == 2:
                self.move_view_pix(self.__prev_cursor_x - event.x, self.__prev_cursor_y - event.y)
                self.__prev_cursor_x = event.x
                self.__prev_cursor_y = event.y

    def __on_press(self, event):
        self.__prev_cursor_x = event.x
        self.__prev_cursor_y = event.y
        self.__is_cursor_held = True
        if event.num == 2:
            self.__held_button = 2
            self['cursor'] = 'fleur'

    def __on_release(self, event):
        self.__is_cursor_held = False
        if event.num == 2:
            self['cursor'] = 'crosshair'
            self.move_view_pix(self.__prev_cursor_x - event.x, self.__prev_cursor_y - event.y)

    def move_view(self, x: float, y: float):
        self.set_view(self.__view_center_x + x, self.__view_center_y + y)

    def move_view_pix(self, x: int, y: int):
        self.move_view(x / self.get_zoom(), y / self.get_zoom())

    def set_view(self, x: float, y: float):
        self.__view_center_x = x
        self.__view_center_y = y
        self.update_content()

    def get_view_x(self):
        return self.__view_center_x

    def get_view_y(self):
        return self.__view_center_y


class MapGrid:
    __workspace: Workspace = None
    __border_id: int = None
    __WH: int = 0
    __vertical_lines_ids: List[int] = []
    __horizontal_lines_ids: List[int] = []

    def __init__(self, workspace: Workspace):
        self.__workspace = workspace
        self.__border_id = workspace.create_rectangle(0, 0, 0, 0, outline='red', width=2)

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
            self.__vertical_lines_ids.append(self.__workspace.create_line(0, 0, 0, 0, fill="red", width=1))
        while len(self.__horizontal_lines_ids) < self.__WH - 1:
            self.__horizontal_lines_ids.append(self.__workspace.create_line(0, 0, 0, 0, fill="red", width=1))
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
