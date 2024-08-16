from Map.MapComponents.MapComponent import *
import math
from Workspace.Drafts.CapturePointDraft import *
from GUI.PropertyInputs.CharPI import CharPI
from GUI.PropertyInputs.PositiveFloatPI import PositiveFloatPI


class CapturePointMapComponent(MapComponent):
    _instances: List = []
    _text_id: int = None
    _base_shape: Point = None
    __d: float = None
    _char: str = None
    _draft: Type[CapturePointDraft] = CapturePointDraft
    _selected_instances: List = []
    _mc_char: str = '*'

    def __init__(self, workspace: IWorkspace, shape: Point, map: IMap, **kwargs):
        super().__init__(workspace, shape, map)
        self._base_shape = shape
        self.__d = kwargs['d']
        self._char = kwargs['char']
        self._shape = shape.buffer(kwargs['d'] / 2)

        self._text_id = workspace.create_text((0, 0), fill="red", font=('Arial',
                                                                        math.ceil(
                                                                            self._workspace.get_zoom() * 160 / 320)),
                                              tags=type(self).__name__, text=self._char)
        self._object_id = workspace.create_oval((0, 0, 0, 0), outline="red",
                                                width=2, tags=type(self).__name__)
        self.update_instance_ct()
        self.update_instance()

    def update_instance(self):
        self._workspace.coords(self._object_id, (
            self._workspace.calc_x(self._base_shape.x - self.__d / 2),
            self._workspace.calc_y(self._base_shape.y - self.__d / 2),
            self._workspace.calc_x(self._base_shape.x + self.__d / 2),
            self._workspace.calc_y(self._base_shape.y + self.__d / 2)
        ))
        self._workspace.coords(self._text_id, (
            self._workspace.calc_x(self._base_shape.x),
            self._workspace.calc_y(self._base_shape.y),
        ))
        self.update_instance_scale()

    def update_instance_scale(self):
        self._workspace.itemconfig(self._text_id, font=('Arial', math.ceil(self._workspace.get_zoom() * 100 / 320)))
        self._workspace.itemconfig(self._object_id, width=2 + 5 * int(self._is_selected))

    def delete(self):
        super().delete()
        self._workspace.delete(self._text_id)

    def move(self, x: float, y: float):
        self._base_shape = Point(self._base_shape.x + x, self._base_shape.y + y)
        self._shape = self._base_shape.buffer(self.__d/2)
        self.update_instance()

    def update_instance_ct(self):
        self._workspace.itemconfig(self._object_id,
                                   width=2 + 5 * int(self._is_selected))

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map: IMap):
        try:
            points = data['*']
            for _ in points:
                cls.new_component(workspace, Point(_[1], _[2]), map, d=_[3], char=_[0])
        except KeyError:
            pass

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/capture_point.png")

    @classmethod
    def new_component(cls, workspace: IWorkspace, shape: Point, map: IMap, **kwargs):
        new_component = cls(workspace, shape, map, **kwargs)
        cls._instances.append(new_component)

        return new_component

    def lift_instance(self):
        super().lift_instance()
        self._workspace.lift(self._text_id)

    @classmethod
    def get_free_char(cls) -> str:
        chars = "ABCDEFGHIJKLMNOPQRSTUVWSYZ"
        for instance in cls._instances:
            chars = chars.replace(instance._char, "")
        return chars[0]

    def select(self):
        super().select()

    def draw_map_instance(self, draw: ImageDraw.Draw, img_wh: int):
        map_wh = self._map.get_wh()
        draw.text((round((self._base_shape.x + self.__d / 2) / map_wh * img_wh),
                   round((self._base_shape.y - self.__d / 2) / map_wh * img_wh) - 5), fill=(255, 0, 0), text=self._char)
        draw.ellipse((round((self._base_shape.x - self.__d / 2) / map_wh * img_wh),
                      round((self._base_shape.y - self.__d / 2) / map_wh * img_wh),
                      round((self._base_shape.x + self.__d / 2) / map_wh * img_wh),
                      round((self._base_shape.y + self.__d / 2) / map_wh * img_wh)), outline=(255, 0, 0), width=2)

    def get_as_list(self) -> List:
        return [self._char, self._base_shape.x, self._base_shape.y, self.__d]

    def set_char(self, char: str):
        chars = "ABCDEFGHIJKLMNOPQRSTUVWSYZ"
        for instance in self._instances:
            chars = chars.replace(instance._char, "")
        print(chars)
        if char in chars:
            self._char = char
            self._workspace.itemconfig(self._text_id, text=char)


    def get_char(self) -> str:
        return self._char

    def set_d(self, d: float):
        self.__d = d
        if self.__d < 0.1:
            self.__d = 0.1
        self.update_instance()
        self.update_instance_scale()
        self._base_shape = Point(self._base_shape.x, self._base_shape.y )
        self._shape = self._base_shape.buffer(self.__d/2)
    def get_d(self):
        return self.__d

    def get_properties(self) -> List[MCProperty]:
        return [
            MCProperty(CharPI, self.set_char, self.get_char, {}, "Name"),
            MCProperty(PositiveFloatPI, self.set_d, self.get_d, {}, "Size")
        ]
