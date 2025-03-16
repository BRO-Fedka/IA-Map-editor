from generator.functions import *


class DecoTree:
    def __init__(self, rr):
        self.valid = False
        self.rr = rr
        self.rock = None
        x = rr.poly.bounds[0] + (rr.poly.bounds[2] - rr.poly.bounds[0]) * random()
        y = rr.poly.bounds[1] + (rr.poly.bounds[3] - rr.poly.bounds[1]) * random()
        while not Point(x, y).intersects(self.rr.poly):
            x = rr.poly.bounds[0] + (rr.poly.bounds[2] - rr.poly.bounds[0]) * random()
            y = rr.poly.bounds[1] + (rr.poly.bounds[3] - rr.poly.bounds[1]) * random()
        sizes_of_stages = {
            0: 0.1,
            1: 0.15,
            2: 0.2,
            3: 0.25,
        }
        self.stage = randint(0, 1)
        r = sizes_of_stages[self.stage] / self.rr.island.world.WH
        if self.rr.island.world.TREETYPE_NOISE([x, y]) + random() * 0.4 - 0.3 > 0:
            self.type = 2
        else:
            self.type = 0
        # if not Point(x, y).intersects(self.rr.poly):
        #     self.valid = False
        #     return
        self.circle = Point(x, y).buffer(r)
        self.point = Point(x, y)
        if self.point.distance(LineString(self.rr.poly.exterior.coords[:] + [
            self.rr.poly.exterior.coords[0]])) < 0.125 / 4 / self.rr.island.world.WH:
            self.valid = False
            return
        # if self.house.intersection(self.rr.poly).area != self.house.area:
        for sh in self.rr.island.BUILT_AREA:
            if self.point.intersects(sh):
                self.valid = False
                return
        for sh in self.rr.ROCK_AREAS:
            if self.point.intersects(sh):
                self.valid = False
                return
        for sh in self.rr.TREE_AREAS:
            if self.point.intersects(sh):
                self.valid = False
                return

        self.valid = True

    def build(self):
        self.rr.TREE_AREAS.append(self.circle)
        self.rr.TREE_POINTS.append(self.point)

    def is_valid(self):
        return self.valid

    def save(self, data):
        data.append([self.type, round(self.point.x * self.rr.island.world.WH, 2),
                     round(self.point.y * self.rr.island.world.WH, 2), self.stage])

    def plot(self):
        pass
