import math
from shapely.geometry import LineString, LinearRing, Polygon, Point
import matplotlib.pyplot as plt


class KeySeaPort:
    def __init__(self, island, seg, no_pier=False):
        self.island = island
        self.valid = False
        self.has_pier = not no_pier
        vec_x = seg.coords[1][0] - seg.coords[0][0]
        vec_y = seg.coords[1][1] - seg.coords[0][1]
        vec_l = math.sqrt(vec_x ** 2 + vec_y ** 2)
        vec_x /= vec_l
        vec_y /= vec_l
        vec_x, vec_y = vec_y, -vec_x
        aver_x = (seg.coords[1][0] + seg.coords[0][0]) / 2
        aver_y = (seg.coords[1][1] + seg.coords[0][1]) / 2
        self.pier_root = Point(aver_x, aver_y)
        pier_len = 0.5 / island.world.WH
        pier_approach = 0.05 / island.world.WH
        sp_wh = 0.75 / island.world.WH
        shift = 0.05 / island.world.WH
        if no_pier:
            self.valid = True
        if self.has_pier:
            if vec_l < 0.2 / island.world.WH:
                print('no SP too small side')
                return
        self.pier_line = LineString([(aver_x - vec_x * pier_approach, aver_y - vec_y * pier_approach),
                                     (aver_x + vec_x * pier_len, aver_y + vec_y * pier_len)])
        self.pier = self.pier_line.buffer(0.1 / island.world.WH, cap_style=2)
        if self.has_pier:
            for i in island.world.ISLANDS:
                if i != self.island and i.poly.buffer(0.5 / island.world.WH).intersects(self.pier):
                    # plt.plot(*i.poly.buffer(0.5 / island.world.WH).exterior.xy,'-c')
                    break
            else:
                self.valid = True
            if not self.valid:
                print('no SP touch isles')
                return
        self.sp_axis_line = LineString([(aver_x + vec_x * pier_len, aver_y + vec_y * pier_len), (
        aver_x - vec_x * (pier_approach + sp_wh), aver_y - vec_y * (pier_approach + sp_wh))])
        self.sp_foundation = self.sp_axis_line.buffer(sp_wh / 2, cap_style=2)
        self.sp_foundation = self.sp_foundation.intersection(self.island.poly)  # .buffer(shift)
        self.sp_foundation = self.sp_foundation.minimum_rotated_rectangle
        self.pier = self.pier.difference(self.sp_foundation)

    def build(self):
        self.island.BUILT_AREA.append(self.sp_foundation.buffer(0.05 / self.island.world.WH))

    def is_valid(self):
        return self.valid

    def plot(self):
        if self.has_pier:
            plt.plot(*self.pier.exterior.xy, '-b')
        plt.plot(*self.sp_foundation.exterior.xy, '-b')

    @staticmethod
    def key(p):
        return p.pier.distance(p.island.aver_center) + 0.5 * ((p.island.poly.centroid.distance(
            LinearRing(p.island.zone.poly.exterior.coords))) - p.pier.centroid.distance(
            LinearRing(p.island.zone.poly.exterior.coords)))
