import math
from shapely.geometry import LineString, LinearRing, Polygon, Point
import matplotlib.pyplot as plt
from generator.functions import *
from generator.Structures.ContainerGrid import ContainerGrid


class BaseCity:
    def __init__(self, island, seg):
        self.island = island
        self.valid = False
        self.road_c_points = []
        vec_x = seg.coords[1][0] - seg.coords[0][0]
        vec_y = seg.coords[1][1] - seg.coords[0][1]
        vec_l = math.sqrt(vec_x ** 2 + vec_y ** 2)
        vec_x /= vec_l
        vec_y /= vec_l

        pvec_x, pvec_y = vec_x, vec_y
        vec_x, vec_y = vec_y, -vec_x
        aver_x = (seg.coords[1][0] + seg.coords[0][0]) / 2
        aver_y = (seg.coords[1][1] + seg.coords[0][1]) / 2
        self.pier_root = Point(aver_x, aver_y)
        pier_len = (0.5 + random() * 0.25) / island.world.WH
        rpier_len = (0.5 + random() * 0.25) / island.world.WH
        lpier_len = (0.5 + random() * 0.25) / island.world.WH
        pier_approach = 0
        sp_w = 4 / island.world.WH
        sp_h = 1 / island.world.WH
        shift = 0.05 / island.world.WH
        self.piers = []
        self.pier_cranes = []
        self.pier_lines = []
        self.pier_line = LineString([(aver_x - vec_x * pier_approach, aver_y - vec_y * pier_approach),
                                     (aver_x + vec_x * pier_len, aver_y + vec_y * pier_len)])
        self.lpier_line = LineString([(aver_x + (2 - 0.15) / island.world.WH * pvec_x - vec_x * pier_approach,
                                       aver_y + (2 - 0.15) / island.world.WH * pvec_y - vec_y * pier_approach),
                                      (aver_x + (2 - 0.15) / island.world.WH * pvec_x + vec_x * lpier_len,
                                       aver_y + (2 - 0.15) / island.world.WH * pvec_y + vec_y * lpier_len)])
        self.rpier_line = LineString([(aver_x - (2 - 0.15) / island.world.WH * pvec_x - vec_x * pier_approach,
                                       aver_y - (2 - 0.15) / island.world.WH * pvec_y - vec_y * pier_approach),
                                      (aver_x - (2 - 0.15) / island.world.WH * pvec_x + vec_x * rpier_len,
                                       aver_y - (2 - 0.15) / island.world.WH * pvec_y + vec_y * rpier_len)])
        self.pier_cranes.append([4,
                                 round((aver_x + vec_x * (pier_len - 0.1 / island.world.WH) + (
                                         pvec_x * 0.04 / island.world.WH)) * island.world.WH, 2),
                                 round((aver_y + vec_y * (
                                         pier_len - 0.1 / island.world.WH) + (
                                                pvec_y * 0.04 / island.world.WH)) * island.world.WH, 2),
                                 0.1, 0.1,
                                 round(lookat(vec_x, vec_y) + 90) % 360])
        self.pier_cranes.append([4,
                                 round((aver_x + vec_x * (pier_len - 0.25 / island.world.WH) + (
                                         pvec_x * -0.04 / island.world.WH)) * island.world.WH, 2),
                                 round((aver_y + vec_y * (
                                         pier_len - 0.25 / island.world.WH) + (
                                                pvec_y * -0.04 / island.world.WH)) * island.world.WH, 2),
                                 0.1, 0.1,
                                 round(lookat(vec_x, vec_y) + 270) % 360])
        self.pier_cranes.append([4,
                                 round((aver_x + vec_x * (lpier_len - 0.1 / island.world.WH) + (
                                         pvec_x * (0.04 + 2 - 0.15) / island.world.WH)) * island.world.WH, 2),
                                 round((aver_y + vec_y * (
                                         lpier_len - 0.1 / island.world.WH) + (
                                                pvec_y * (0.04 + 2 - 0.15) / island.world.WH)) * island.world.WH, 2),
                                 0.1, 0.1,
                                 round(lookat(vec_x, vec_y) + 90) % 360])
        self.pier_cranes.append([4,
                                 round((aver_x + vec_x * (lpier_len - 0.25 / island.world.WH) + (
                                         pvec_x * (-0.04 + 2 - 0.15) / island.world.WH)) * island.world.WH, 2),
                                 round((aver_y + vec_y * (
                                         lpier_len - 0.25 / island.world.WH) + (
                                                pvec_y * (-0.04 + 2 - 0.15) / island.world.WH)) * island.world.WH, 2),
                                 0.1, 0.1,
                                 round(lookat(vec_x, vec_y) + 270) % 360])
        self.pier_cranes.append([4,
                                 round((aver_x + vec_x * (rpier_len - 0.1 / island.world.WH) + (
                                         pvec_x * (0.04 - 2 + 0.15) / island.world.WH)) * island.world.WH, 2),
                                 round((aver_y + vec_y * (
                                         rpier_len - 0.1 / island.world.WH) + (
                                                pvec_y * (0.04 - 2 + 0.15) / island.world.WH)) * island.world.WH, 2),
                                 0.1, 0.1,
                                 round(lookat(vec_x, vec_y) + 90) % 360])
        self.pier_cranes.append([4,
                                 round((aver_x + vec_x * (rpier_len - 0.25 / island.world.WH) + (
                                         pvec_x * (-0.04 - 2 + 0.15) / island.world.WH)) * island.world.WH, 2),
                                 round((aver_y + vec_y * (
                                         rpier_len - 0.25 / island.world.WH) + (
                                                pvec_y * (-0.04 - 2 + 0.15) / island.world.WH)) * island.world.WH, 2),
                                 0.1, 0.1,
                                 round(lookat(vec_x, vec_y) + 270) % 360])
        self.pier = self.pier_line.buffer(0.15 / island.world.WH, cap_style=2)
        self.lpier = self.lpier_line.buffer(0.15 / island.world.WH, cap_style=2)
        self.rpier = self.rpier_line.buffer(0.15 / island.world.WH, cap_style=2)
        for i in island.world.ISLANDS:
            buf = i.poly.buffer(0.5 / island.world.WH)
            if i != self.island and (
                    buf.intersects(self.pier) or buf.intersects(self.lpier) or buf.intersects(self.rpier)):
                # plt.plot(*i.poly.buffer(0.5 / island.world.WH).exterior.xy,'-c')
                self.valid = False
                return
        else:
            pass
        for _ in range(0, 2):
            iters = 100
            while iters > 0:
                pos = (-2 + random() * 4)
                ln = (0.5 + random() * 0.25) / island.world.WH
                pier_line = LineString([(aver_x + pos / island.world.WH * pvec_x - vec_x * pier_approach,
                                         aver_y + pos / island.world.WH * pvec_y - vec_y * pier_approach),
                                        (aver_x + pos / island.world.WH * pvec_x + vec_x * ln,
                                         aver_y + pos / island.world.WH * pvec_y + vec_y * ln)])
                pier = pier_line.buffer(0.15 / island.world.WH, cap_style=2)
                for i in island.world.ISLANDS:
                    buf = i.poly.buffer(0.5 / island.world.WH)
                    if i != self.island and (buf.intersects(pier)):
                        # plt.plot(*i.poly.buffer(0.5 / island.world.WH).exterior.xy,'-c')
                        break
                else:
                    buf = pier.buffer(0.35 / island.world.WH)
                    if not (buf.intersects(self.pier) or buf.intersects(self.lpier) or buf.intersects(self.rpier)):
                        for p in self.piers:
                            if buf.intersects(p):
                                break
                        else:
                            self.pier_lines.append(pier_line)
                            self.piers.append(pier)
                            self.pier_cranes.append([4,
                                                     round((aver_x + vec_x * (ln - 0.1 / island.world.WH) + (
                                                             pvec_x * (
                                                             0.04 + pos) / island.world.WH)) * island.world.WH,
                                                           2),
                                                     round((aver_y + vec_y * (
                                                             ln - 0.1 / island.world.WH) + (
                                                                    pvec_y * (
                                                                    0.04 + pos) / island.world.WH)) * island.world.WH,
                                                           2),
                                                     0.1, 0.1,
                                                     round(lookat(vec_x, vec_y) + 90) % 360])
                            self.pier_cranes.append([4,
                                                     round((aver_x + vec_x * (ln - 0.25 / island.world.WH) + (
                                                             pvec_x * (
                                                             -0.04 + pos) / island.world.WH)) * island.world.WH,
                                                           2),
                                                     round((aver_y + vec_y * (
                                                             ln - 0.25 / island.world.WH) + (
                                                                    pvec_y * (
                                                                    -0.04 + pos) / island.world.WH)) * island.world.WH,
                                                           2),
                                                     0.1, 0.1,
                                                     round(lookat(vec_x, vec_y) + 270) % 360])
                            break

            if iters == 0:
                self.valid = False
                return
        # if not self.valid:
        #     print('no SP touch isles')
        #     return
        self.sp_axis_line = LineString([(aver_x + vec_x * pier_len, aver_y + vec_y * pier_len), (
            aver_x - vec_x * (pier_approach + sp_h), aver_y - vec_y * (pier_approach + sp_h))])
        self.sp_foundation = self.sp_axis_line.buffer(sp_w / 2, cap_style=2)
        self.sp_foundation = self.sp_foundation.intersection(self.island.poly)  # .buffer(shift)
        self.sp_foundation = self.sp_foundation.minimum_rotated_rectangle
        self.cgs = []
        self.hangars = []
        for i in range(-2, 3):
            self.hangars.append([3,
                                 round((aver_x - vec_x * (pier_approach + (1 - 0.02 - 0.4 / 2) / island.world.WH) + (
                                         pvec_x * i*0.89 / island.world.WH)) * island.world.WH, 2),
                                 round((aver_y - vec_y * (pier_approach + (1 - 0.02 - 0.4 / 2) / island.world.WH) + (
                                         pvec_y * i*0.89 / island.world.WH)) * island.world.WH, 2),
                                 0.4, 0.35,
                                 round(lookat(vec_x, vec_y))])
        for i in range(-2, 2):
            cg_axis_line = LineString([(aver_x - (pvec_x * (1 * i + 0.5) / island.world.WH),
                                        aver_y - (pvec_y * (1 * i + 0.5) / island.world.WH)),
                                       (aver_x - vec_x * (0.4 / island.world.WH) - (
                                               pvec_x * (1 * i + 0.5) / island.world.WH),
                                        aver_y - (pvec_y * (1 * i + 0.5) / island.world.WH) - vec_y *
                                        (0.4 / island.world.WH))])
            cg_zone = cg_axis_line.buffer(0.5 / 2 / island.world.WH, cap_style=2)
            cg_zone = cg_zone.intersection(self.sp_foundation)  # .buffer(shift)
            self.cgs.append(ContainerGrid(cg_zone, island).get_as_list())
        self.pier = self.pier.difference(self.sp_foundation)
        self.city_axis_line = LineString(
            [(aver_x - vec_x * 0.75 / island.world.WH, aver_y - vec_y * 0.75 / island.world.WH), (
                aver_x - vec_x * (3 + 0.75) / island.world.WH, aver_y - vec_y * (3 + 0.75) / island.world.WH)])
        self.city_foundation = self.city_axis_line.buffer(6 / 2 / island.world.WH, cap_style=2)
        if not (not self.city_foundation.intersects(
                self.island.world.MAP_SQUARE_LS) and self.city_foundation.intersects(
            self.island.world.MAP_SQUARE)):
            self.valid = False
            return
        px = [-3, 3]
        for x in range(0, 6):
            iter = 10
            while iter > 0:
                iter -= 1
                tx = random() * 6 - 3
                for cx in px:
                    if abs(cx - tx) < 0.4:
                        break
                else:
                    iter = 0
                    px.append(tx)
        py = [0, 3]
        for y in range(0, 3):
            iter = 10
            while iter > 0:
                iter -= 1
                ty = random() * 3
                for cy in py:
                    if abs(cy - ty) < 0.4:
                        break
                else:
                    iter = 0
                    py.append(ty)
        px.sort()
        py.sort()
        # print("QUARTERS !")
        # print(px)
        # print(py)
        for x in px:  # range(-3, 4):
            for y in py:  # range(0, 4):
                self.road_c_points.append((aver_x - vec_x * (0.75 + y) / island.world.WH + pvec_x * x / island.world.WH,
                                           aver_y + pvec_y * x / island.world.WH - vec_y * (
                                                   0.75 + y) / island.world.WH))

        self.valid = True

    def save(self, data):
        if not "C" in data.keys():
            data['C'] = []
        data['C'].append(list(
            map(lambda v: list(map(lambda g: round(g * self.island.world.WH, 2), v)), self.pier.exterior.coords[:])))
        data['C'].append(list(
            map(lambda v: list(map(lambda g: round(g * self.island.world.WH, 2), v)), self.lpier.exterior.coords[:])))
        data['C'].append(list(
            map(lambda v: list(map(lambda g: round(g * self.island.world.WH, 2), v)), self.rpier.exterior.coords[:])))
        for p in self.piers:
            data['C'].append(
                list(map(lambda v: list(map(lambda g: round(g * self.island.world.WH, 2), v)), p.exterior.coords[:])))
        data['C'].append(list(map(lambda v: list(map(lambda g: round(g * self.island.world.WH, 2), v)),
                                  self.sp_foundation.exterior.coords[:])))
        if not "#" in data.keys():
            data['#'] = []
        data['#'].append(self.pier_cranes+self.hangars)
        for cg in self.cgs:
            data['#'].append(cg)

    def build(self):
        self.island.BUILT_AREA.append(self.sp_foundation.buffer(0.05 / self.island.world.WH))
        self.island.CITY_AREA.append(self.city_foundation.buffer(0.05 / self.island.world.WH))

    def is_valid(self):
        return self.valid

    def plot(self):

        plt.plot(*self.pier.exterior.xy, '-b')
        plt.plot(*self.rpier.exterior.xy, '-b')
        plt.plot(*self.lpier.exterior.xy, '-b')
        plt.plot(*self.city_foundation.exterior.xy, '-b')
        for p in self.piers:
            plt.plot(*p.exterior.xy, '-b')
        plt.plot(*self.sp_foundation.exterior.xy, '-b')

    @staticmethod
    def key(p):
        return p.pier.distance(p.island.aver_center) + 0.5 * ((p.island.poly.centroid.distance(
            LinearRing(p.island.zone.poly.exterior.coords))) - p.pier.centroid.distance(
            LinearRing(p.island.zone.poly.exterior.coords)))
