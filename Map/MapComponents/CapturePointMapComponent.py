from Map.MapComponents.MapComponent import *
import math


class BridgeMapComponent(MapComponent):
    _instances: List = []
    _text_id: int = None
    _base_shape: Point = None
    __d: float = None
    __char: str = None

    def __init__(self, workspace: IWorkspace, shape: Point, map: IMap, **kwargs):
        super().__init__(workspace, shape, map)
        self._base_shape = shape
        self.__d = kwargs['d']
        self.__char = kwargs['char']
        self._shape = shape.buffer(kwargs['d'])

        self._text_id = workspace.create_text((0, 0), fill="red", font=('Arial',
                                                                            math.ceil(self._workspace.get_zoom() * 160 / 320)),
                                              tags=type(self).__name__,text=self.__char)
        self._object_id = workspace.create_oval((0, 0, 0, 0), outline="red",
                                                width=2, tags=type(self).__name__)

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
        self._workspace.itemconfig(self._text_id, font=('Arial', math.ceil(self._workspace.get_zoom() * 120 / 320)))
        self._workspace.itemconfig(self._object_id, width=2 + 5 * int(self._is_selected))

    def delete(self):
        super().delete()
        self._workspace.delete(self._text_id)

    def move(self, x: float, y: float):
        self._base_shape = Point(self._base_shape.x + x, self._base_shape.y + y)
        self._shape = self._base_shape.buffer(self.__d)
        self.update_instance()

    def update_instance_ct(self):
        self._workspace.itemconfig(self._object_id,
                                   width=2 + 5 * int(self._is_selected))

    @classmethod
    def parse_map_raw_data_create_all(cls, data: dict, workspace: IWorkspace, map: IMap):
        try:
            points = data['*']
            for _ in points:
                print([(_[0], _[1]), (_[2], _[3])])
                cls.new_component(workspace, Point(_[1], _[2]), map,d=_[3], char =_[0])
        except KeyError:
            pass

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/capture_point.png")

    @classmethod
    def new_component(cls, workspace: IWorkspace, shape: Point, map: IMap,**kwargs):
        new_component = cls(workspace, shape, map, **kwargs)
        cls._instances.append(new_component)

        return new_component