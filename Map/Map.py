from typing import *

import svgwrite.shapes
import time
from Map.IMap import *
from functions.functions import *
import json
from Map.MapComponents.MapComponent import *
from Map.MapComponents.PolyMapComponent import PolyMapComponent
from Map.MapComponents.BeachMapComponent import BeachMapComponent
from Map.MapComponents.GrassMapComponent import GrassMapComponent
from Map.MapComponents.RoadMapComponent import RoadMapComponent
from Map.MapComponents.BridgeMapComponent import BridgeMapComponent
from Map.MapComponents.ConcreteMapComponent import ConcreteMapComponent
from Map.MapComponents.StoneMapComponent import StoneMapComponent
from Map.MapComponents.CapturePointMapComponent import CapturePointMapComponent
from Map.MapComponents.VehicleDummyMapComponent import VehicleDummyMapComponent
from Map.MapComponents.BuildingsMapComponent import BuildingsMapComponent
from Map.MapComponents.TreesMapComponent import TreesMapComponent

from svgwrite import Drawing
import webbrowser
from PIL import Image, ImageDraw, ImageFilter
from functions.functions import hex_to_rgb
import os


class Map(IMap):
    __workspace: IWorkspace = None
    __data: Dict = {}
    __available_map_components: List[Type[MapComponent]]
    __ct: Dict[str, str] = None
    __wh: int = None
    __file_path: str = None

    def __init__(self, data: dict, workspace: IWorkspace, fp: str = None):
        self.__data = data
        self.__file_path = fp
        self.__available_map_components = get_finite_inherits(MapComponent)
        self.__ct = data['CT']
        self.__wh = data['WH']
        self.__workspace = workspace
        for mc in self.__available_map_components:
            mc.parse_map_raw_data_create_all(data, workspace, self)
        self.update_ct()
        self.update_layer_sequence()

    def update_layer_sequence(self):
        self.__workspace.lift('shore0')
        self.__workspace.lift('shore1')
        for mc in self.__available_map_components:
            mc.lift()
        self.__workspace.lift('markers')

    def update_ct(self):
        for mc in self.__available_map_components:
            mc.update_ct()

    def update(self, x0: float = None, x1: float = None, y0: float = None, y1: float = None):
        for mc in self.__available_map_components:
            start = time.time()
            mc.update(x0=x0,x1=x1,y0=y0,y1=y1)
            end = time.time()
            # print((end - start) * 1000, mc.__name__)

    def load_ct(self, fp: str):
        with open(fp) as file:
            parsed_json = json.load(file)
            self.__ct = parsed_json['CT']
            self.update_ct()
            self.__workspace.set_bg(self.get_ct_field('bg'))

    def save_ct(self, fp: str):
        with open(fp, 'w') as file:
            json.dump({'CT': self.__ct}, file)

    def get_ct_field(self, key: str) -> str:
        try:
            return self.__ct[key]
        except KeyError:
            self.__ct[key] = '#000'
            return '#000'

    def set_ct_field(self, key: str, val: str):
        self.__ct[key] = val
        self.update_ct()
        self.__workspace.set_bg(self.get_ct_field('bg'))

    def get_ct_copy(self) -> Dict[str, str]:
        return self.__ct.copy()

    def get_wh(self) -> int:
        return self.__wh

    @classmethod
    def from_json_file(cls, fp: str, workspace: IWorkspace):
        with open(fp) as file:
            parsed_json = json.load(file)
            new_map = Map(parsed_json, workspace, fp=fp)
            return new_map

    @classmethod
    def new_map(cls, wh: int, ct_fp: str, workspace: IWorkspace):
        with open(ct_fp) as file:
            parsed_json = json.load(file)
            parsed_json['WH'] = wh
            new_map = Map(parsed_json, workspace)
            return new_map

    def get_preview_image_draw(self, wh: int = 640, blur: bool = False):
        img = Image.new("RGB", size=(wh, wh), color=hex_to_rgb(self.get_ct_field('bg')))
        draw = ImageDraw.Draw(img)
        draw.antialias = True

        for mc in self.__available_map_components:
            mc.draw_map_image_draw(draw, wh)
        img = img.filter(ImageFilter.BoxBlur(int(blur)))
        img.save(os.getcwd() + '/Output/output.png')

    def get_preview_image_svg(self, wh: int = 640):
        draw = Drawing(os.getcwd() + "/Output/output.svg")
        rect = draw.add(svgwrite.shapes.Rect((0, 0), (wh, wh)))
        rect.fill(self.get_ct_field('bg'))
        for mc in self.__available_map_components:
            mc.draw_map_svgwrite(draw, wh)
        draw.save()
        try:
            webbrowser.open(os.getcwd() + "/Output/output.svg")
        except:
            pass

    def close(self):
        for mc in self.__available_map_components:
            mc.delete_all()

    def get_fp(self):
        return self.__file_path

    def save_to_json_file(self, fp: str = None):
        if fp is None:
            if self.__file_path is None:
                raise ValueError
            else:
                fp = self.__file_path
        else:
            self.__file_path = fp
        q = []
        map_data = {
            'WH': self.get_wh(),
            'CT': self.__data['CT']
        }
        q_cols = {}
        for x in range(0, self.get_wh()):
            q.append([])
            for y in range(0, self.get_wh()):
                q[x].append({})
                q_cols[(x, y)] = Polygon([(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)])
        for mc in self.__available_map_components:
            mc.fill_q(q, q_cols, self.get_wh())
            mc.fill_data(map_data)
        map_data['Q'] = q
        with open(self.__file_path, 'w') as file:
            json.dump(map_data, file)
