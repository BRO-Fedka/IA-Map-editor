from Workspace.Drafts.Draft import *
from Workspace.MapGrid import *
from GUI.ICommon import *
import keyboard

MOVE: int = 2
SELECT: int = 3
INTERACT: int = 1


class Workspace(IWorkspace, ICommon):
    __map: [IMap, None] = None
    __zoom: float = 320
    __view_center_x: float = 0
    __view_center_y: float = 0
    __prev_cursor_x: float = 0
    __prev_cursor_y: float = 0
    __is_cursor_held: bool = False
    __held_button: int = 0
    __def_bg: str = "#eee"
    __draft: [Draft, None] = None

    def __init__(self, master: Optional[Misc], **kwargs):
        super().__init__(master, kwargs)
        self['highlightthickness'] = 0
        self['cursor'] = 'crosshair'
        self.__grid: MapGrid = MapGrid(self)
        self.__grid.set_wh(16)
        try:
            self.__def_bg = self['bg']
        except KeyError:
            pass
        self.update_content()
        self.bind('<MouseWheel>', self.__on_wheel)
        self.bind('<Configure>', self.__on_configure)
        self.bind('<Motion>', self.__on_motion)
        self.bind("<ButtonPress>", self.__on_press)
        self.bind("<ButtonRelease>", self.__on_release)
        self.bind(f"<Double-Button-{SELECT}>", self.__on_dbl_click)
        keyboard.add_hotkey('delete', self.__on_del)

    def set_map(self, map: IMap):
        self.__map = map
        self.update_map()
        self.__grid.lift()
        self.master.get_info_widget().update_wh(map.get_wh())

    def get_map(self) -> IMap:
        return self.__map

    def update_map(self):
        if self.__map is None:
            self['bg'] = self.__def_bg
        else:
            self['bg'] = self.__map.get_ct_field('bg')
            self.__map.update()
            self.__grid.set_wh(self.get_map().get_wh())

    def update_content(self):
        self.__grid.update()
        self.update_map()
        if self.has_draft():
            self.get_draft().update()

    def update_layers(self):
        self.get_map().update_layer_sequence()
        self.__grid.lift()

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
        map_x, map_y = self.get_game_coords_from_pix(event.x, event.y)
        self.get_info_widget().update_x(map_x)
        self.get_info_widget().update_y(map_y)
        if self.__is_cursor_held:
            if self.__held_button == MOVE:
                self.move_view_pix(self.__prev_cursor_x - event.x, self.__prev_cursor_y - event.y)
                self.__prev_cursor_x = event.x
                self.__prev_cursor_y = event.y
            elif self.__held_button == INTERACT and not self.has_draft():
                self.get_mc_menu().get_selected_map_component().move_selected(
                    (-self.__prev_cursor_x + event.x) / self.get_zoom(),
                    (-self.__prev_cursor_y + event.y) / self.get_zoom())
                self.__prev_cursor_x = event.x
                self.__prev_cursor_y = event.y

    def __on_press(self, event):
        self.__on_click(event)
        if not self.__is_cursor_held:
            self.__prev_cursor_x = event.x
            self.__prev_cursor_y = event.y
            self.__is_cursor_held = True
            self.__held_button = event.num
            print(event.num)
            if event.num == MOVE:
                self['cursor'] = 'fleur'
            elif event.num == INTERACT and not self.has_draft():

                self['cursor'] = 'plus'

    def __on_release(self, event):
        self.__is_cursor_held = False
        self['cursor'] = 'crosshair'
        if event.num == MOVE:
            self.move_view_pix(self.__prev_cursor_x - event.x, self.__prev_cursor_y - event.y)

    def __on_click(self, event):
        if self.has_draft():
            if event.num == SELECT:
                self.get_draft().select_btn(*self.get_game_coords_from_pix(event.x, event.y))
            elif event.num == INTERACT:
                self.get_draft().interact_btn(*self.get_game_coords_from_pix(event.x, event.y))
        else:
            print('1-')
            if event.num == SELECT:
                self.get_mc_menu().get_selected_map_component().select_at_coords(
                    *self.get_game_coords_from_pix(event.x, event.y))

    def __on_dbl_click(self, event):
        self.new_draft(*self.get_game_coords_from_pix(event.x, event.y))

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

    def get_game_coords_from_pix(self, x: int, y: int) -> Coords:
        zoom = self.get_zoom()
        return Coords(x=round((x - (-self.get_view_x() * zoom + self.winfo_width() / 2)) / zoom, 2),
                      y=round((y - (-self.get_view_y() * zoom + self.winfo_height() / 2)) / zoom, 2))

    def __on_del(self):
        self.get_mc_menu().get_selected_map_component().delete_selected()

    def has_draft(self) -> bool:
        # print('draft',self.__draft)
        if self.__draft is None:
            return False
        else:
            print(self.get_draft())
            return True

    def get_draft(self) -> [Draft, None]:
        return self.__draft

    def new_draft(self, x: float, y: float):
        if self.get_map() is None:
            return
        if self.has_draft():
            self.get_draft().complete()
        self.__draft = self.get_mc_menu().get_selected_map_component().get_draft()(self.get_map(), self,
                                                                                   self.get_mc_menu().get_selected_map_component(),
                                                                                   x, y)

    def remove_draft(self):
        self.__draft = None

