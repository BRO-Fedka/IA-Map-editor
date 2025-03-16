from generator.functions import *


class Tree:
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
        self.stage = randint(1, 5)
        if self.stage == 5:
            if random() > 0.5:
                self.stage = 0
            else:
                self.stage = 3
        else:
            self.stage = math.ceil(self.stage / 2)
        r = sizes_of_stages[self.stage] / self.rr.island.world.WH
        if self.rr.island.world.TREETYPE_NOISE([x, y]) + random() * 0.4 - 0.3 > 0:
            self.type = 0
        else:
            self.type = 1
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
        ta = 0
        for sh in self.rr.TREE_AREAS:
            if self.point.intersects(sh):
                ta += 1
                if ta > 3:
                    break
        if ta == 0:
            if random() > 0.5:
                self.valid = False
                return
        else:
            if ta > 3:
                self.valid = False
                return
        for p in self.rr.TREE_POINTS:
            if self.point.distance(p) < 0.02 / self.rr.island.world.WH:
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
        # plt.plot(*self.rock.exterior.xy, '-k')
