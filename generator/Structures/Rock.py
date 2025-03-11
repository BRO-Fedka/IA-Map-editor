import math
from shapely.geometry import LineString, LinearRing, Polygon, Point
import matplotlib.pyplot as plt
from generator.functions import *


class Rock:
    def __init__(self, rr):
        self.valid = False
        self.rr = rr
        self.rock = None
        x = rr.poly.bounds[0] + (rr.poly.bounds[2] - rr.poly.bounds[0]) * random()
        y = rr.poly.bounds[1] + (rr.poly.bounds[3] - rr.poly.bounds[1]) * random()
        while not Point(x, y).intersects(self.rr.poly):
            x = rr.poly.bounds[0] + (rr.poly.bounds[2] - rr.poly.bounds[0]) * random()
            y = rr.poly.bounds[1] + (rr.poly.bounds[3] - rr.poly.bounds[1]) * random()
        r = (random() * 0.3 + 0.1) / self.rr.island.world.WH
        # if not Point(x, y).intersects(self.rr.poly):
        #     self.valid = False
        #     return
        self.circle = Point(x, y).buffer(r)
        if self.circle.distance(LineString(self.rr.poly.exterior.coords[:] + [
            self.rr.poly.exterior.coords[0]])) < 0.125 / 4 / self.rr.island.world.WH:
            self.valid = False
            return
        # if self.house.intersection(self.rr.poly).area != self.house.area:
        for sh in self.rr.island.BUILT_AREA:
            if self.circle.intersects(sh):
                self.valid = False
                return
        for sh in self.rr.ROCK_AREAS:
            d = sh.distance(self.circle)
            if self.circle.intersects(sh):
                intr = self.circle.intersection(sh)
                cof = intr.area / self.circle.area
                if sh.area < self.circle.area or cof > 0.25 or cof < 0.05:
                    self.valid = False
                    return

            elif 0 < d < 0.03 / self.rr.island.world.WH:
                self.valid = False
                return

        self.valid = True
        while True:
            vertsamnt = max(7,randint(math.ceil(r/0.1/self.rr.island.world.WH*3.5),math.ceil(r/0.1/self.rr.island.world.WH*5)))
            verts = []
            for _ in range(vertsamnt):
                deg = random()*2*math.pi
                verts.append([deg,(x+math.cos(deg)*r,y+math.sin(deg)*r)])
            verts.sort()
            verts = list(map(lambda e: e[1],verts))
            self.rock = Polygon(verts)
            if self.rock.area/self.circle.area>0.7:
                break

    def build(self):
        self.rr.ROCK_AREAS.append(
            self.circle)  # self.house.buffer(0.02/2 / self.rr.island.world.WH)

    def is_valid(self):
        return self.valid

    def plot(self):
        plt.plot(*self.rock.exterior.xy, '-k')

    def save(self,data):
        if not "S" in data.keys():
            data['S'] = []
        data['S'].append(list(map(lambda v: list(map(lambda g: round(g*self.rr.island.world.WH, 2), v)), self.rock.exterior.coords[:])))


