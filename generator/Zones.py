from generator.functions import *
from generator.Islands.Island import Island
from generator.Islands.BaseIsland import BaseIsland
from generator.Islands.ArchIsland import ArchIsland
from generator.Islands.KeyIsland import KeyIsland

class Zone:
    def __init__(self, x: float, y: float, poly: Polygon, world):
        self.x = x
        self.y = y
        self.poly = poly
        self.near_zones = []
        self.ratio = max((self.poly.bounds[3] - self.poly.bounds[1]) / (self.poly.bounds[2] - self.poly.bounds[0]),
                         (self.poly.bounds[2] - self.poly.bounds[0]) / (self.poly.bounds[3] - self.poly.bounds[1]))
        self.stones = []

    def generate(self, stage, world):
        if type(self) == Zone:
            if (self.x == 0.1 and self.y == 0.1) or (self.x == 0.9 and self.y == 0.9) and stage == 0:
                world.ZONES.append(BaseZone(self.x, self.y, self.poly, world))
                world.ZONES.remove(self)
                del self
                return
            elif stage > 0:
                zonescls = [ArchipelagoZone, ArchipelagoZone, IslandZone, IslandZone][::-1]
                world.ZONES.append(zonescls[world.AREAS.index(self) // 3](self.x, self.y, self.poly, world))
                world.ZONES.remove(self)
                del self
                return

    def plot(self):
        for s in self.stones:
            plt.plot(s.x, s.y, '.m')
        plt.plot(*self.poly.centroid.xy, 'xb')
        # plt.plot(self.x, self.y, '.b')


class BaseZone(Zone):
    def __init__(self, x, y, poly, world):
        super().__init__(x, y, poly, world)
        world.BASES.append(self)
        ln = LinearRing(list(self.poly.exterior.coords[:]))
        dst = 1
        pnt = None
        if x == 0.1:
            pnt = Point(0, 0)
        else:
            pnt = Point(1, 1)
        for line in segments(ln):
            if line.intersects(pnt):
                # print('!')
                continue
            dst = min(pnt.distance(line), dst)
        islands = []
        island = None
        for _ in range(0, 100):
            flag = False
            size = randint(6, 9) * 0.1
            iter = 0
            while not flag:
                if iter > 1000:
                    flag = True
                iter += 1
                try:
                    p = generatePolygon2(generatePolygon(pnt.x, pnt.y, dst * size, 0.5, 0.5,
                                                         round(10 * max(1, (self.poly.area / 0.05) ** 0.5))))
                    for _ in range(0, 2):
                        p = smoothPolygon(p, 2)
                    for _ in range(0, 2):
                        p = smoothPolygon(p, 1)

                    island = Polygon(p)
                    # if not island.is_valid():
                    #     continue

                    if not world.MAP_SQUARE.difference(self.poly).intersects(island):
                        # print('LOL')
                        segs = segments(LinearRing(list(island.exterior.coords[:])))
                        if island.intersection(world.MAP_SQUARE).area / self.poly.area > 0.7:
                            continue
                        for l in range(0, len(segs)):
                            vec0 = [segs[l].coords[1][0] - segs[l].coords[0][0],
                                    segs[l].coords[1][1] - segs[l].coords[0][1]]
                            vec1 = [segs[(l + 1) % len(segs)].coords[1][0] - segs[(l + 1) % len(segs)].coords[0][0],
                                    segs[(l + 1) % len(segs)].coords[1][1] - segs[(l + 1) % len(segs)].coords[0][1]]
                            len_vec0 = math.sqrt(vec0[0] ** 2 + vec0[1] ** 2)
                            len_vec1 = math.sqrt(vec1[0] ** 2 + vec1[1] ** 2)
                            cos = (vec0[0] * vec1[0] + vec0[1] * vec1[1]) / len_vec0 / len_vec1
                            if cos <= 0:
                                print("island seg cos < 0")
                                break
                        else:
                            flag = True
                except:
                    pass
            if iter < 1000:
                islands.append(island)
        self.island = max(islands, key=lambda i: i.intersection(world.MAP_SQUARE).area)
        world.ISLANDS.append(BaseIsland(self.island,world,self)) #BaseIsland

    def plot(self):
        super().plot()
        plt.plot(*self.poly.exterior.xy, '-r')
        plt.plot(self.x, self.y, 'xr')
        # plt.plot(*self.island.exterior.xy, '-k')


class IslandZone(Zone):
    def __init__(self, x, y, poly, world):
        super().__init__(x, y, poly, world)
        print(self.poly.area)
        ln = LinearRing(list(self.poly.exterior.coords[:]))
        dst = 1
        for line in segments(ln):
            dst = min(self.poly.centroid.distance(line), dst)
        center = self.poly.centroid
        islands = []
        island = None
        for _ in range(0, 30):  # randint(5, 20)
            flag = False
            size = randint(3, 6) * 0.1
            while not flag:
                try:

                    # print(ln)
                    # print(self.poly)

                    p = generatePolygon2(generatePolygon(center.x, center.y, dst * size, 0.5, 0.5,
                                                         round(10 * max(1, self.poly.area / 0.05))))
                    for _ in range(0, 2):
                        p = smoothPolygon(p, 2)
                    for _ in range(0, 2):
                        p = smoothPolygon(p, 1)

                    island = Polygon(p)
                    # if not island.is_valid():
                    #     continue
                    if self.poly.intersection(island).area == island.area:
                        segs = segments(LinearRing(list(island.exterior.coords[:])))
                        for l in range(0, len(segs)):
                            vec0 = [segs[l].coords[1][0] - segs[l].coords[0][0],
                                    segs[l].coords[1][1] - segs[l].coords[0][1]]
                            vec1 = [segs[(l + 1) % len(segs)].coords[1][0] - segs[(l + 1) % len(segs)].coords[0][0],
                                    segs[(l + 1) % len(segs)].coords[1][1] - segs[(l + 1) % len(segs)].coords[0][1]]
                            len_vec0 = math.sqrt(vec0[0] ** 2 + vec0[1] ** 2)
                            len_vec1 = math.sqrt(vec1[0] ** 2 + vec1[1] ** 2)
                            cos = (vec0[0] * vec1[0] + vec0[1] * vec1[1]) / len_vec0 / len_vec1
                            if cos <= 0:
                                print("island seg cos < 0")
                                break
                        else:
                            flag = True
                except:
                    pass
            islands.append(island)
        self.island = max(islands, key=lambda i: i.area)
        world.ISLANDS.append(KeyIsland(self.island,world,self))

    def plot(self):
        super().plot()
        plt.plot(*self.poly.exterior.xy, ':r')
        plt.plot(self.x, self.y, '.r')
        # plt.plot(*self.island.exterior.xy, '-k')


class ArchipelagoZone(Zone):
    def __init__(self, x, y, poly, world):
        super().__init__(x, y, poly, world)

        islands = []
        island = None
        print(self.poly.area)
        for _ in range(0, 30):
            flag = False
            size = randint(5, 7) * 0.1
            while not flag:
                try:
                    ln = LinearRing(list(self.poly.exterior.coords[:]))
                    dst = 1
                    for line in segments(ln):
                        dst = min(self.poly.centroid.distance(line), dst)
                    # print(ln)
                    # print(self.poly)
                    center = self.poly.centroid
                    p = generatePolygon2(generatePolygon(center.x, center.y, dst * size, 0.5, 0.5, round(
                        10 * max(1, self.poly.area / 0.05) ** 0.75)))  # randint(10, 30)
                    for _ in range(0, 2):
                        p = smoothPolygon(p, 2)
                    for _ in range(0, 2):
                        p = smoothPolygon(p, 1)

                    island = Polygon(p)
                    # if not island.is_valid():
                    #     continue
                    if self.poly.intersection(island).area == island.area:
                        segs = segments(LinearRing(list(island.exterior.coords[:])))
                        for l in range(0, len(segs)):
                            vec0 = [segs[l].coords[1][0] - segs[l].coords[0][0],
                                    segs[l].coords[1][1] - segs[l].coords[0][1]]
                            vec1 = [segs[(l + 1) % len(segs)].coords[1][0] - segs[(l + 1) % len(segs)].coords[0][0],
                                    segs[(l + 1) % len(segs)].coords[1][1] - segs[(l + 1) % len(segs)].coords[0][1]]
                            len_vec0 = math.sqrt(vec0[0] ** 2 + vec0[1] ** 2)
                            len_vec1 = math.sqrt(vec1[0] ** 2 + vec1[1] ** 2)
                            cos = (vec0[0] * vec1[0] + vec0[1] * vec1[1]) / len_vec0 / len_vec1
                            if cos <= 0:
                                print("island seg cos < 0")
                                break
                        else:
                            flag = True
                except:
                    pass
            islands.append(island)
        self.island = max(islands, key=lambda i: i.area)

        self.subislands = []
        for _ in range(0, randint(1, 4)):
            flag = False
            size = randint(2, 4) * 0.1
            island = None
            iters = 0
            while not flag and iters < 10000:
                iters += 1
                try:
                    deg = random() * 2 * math.pi
                    l = dst * (0.25 + random() * 1.5)
                    x = center.x + math.cos(deg) * l
                    y = center.y + math.sin(deg) * l
                    p = generatePolygon2(generatePolygon(x, y, dst * size, 0.5, 0.5, 10))
                    for _ in range(0, 2):
                        p = smoothPolygon(p, 2)
                    for _ in range(0, 2):
                        p = smoothPolygon(p, 1)

                    island = Polygon(p)
                    # print('i')
                    # if not island.is_valid():
                    #     continue

                    if not self.island.intersects(island.buffer(0.5 / world.WH)):
                        if self.poly.intersection(island.buffer(0.25 / world.WH)).area == island.buffer(
                                0.25 / world.WH).area:
                            for i in self.subislands:
                                if i.intersects(island.buffer(0.5 / world.WH)):
                                    break
                            else:
                                for i in self.subislands + [self.island]:
                                    if i.distance(island) < 0.75 / world.WH:
                                        segs = segments(LinearRing(list(island.exterior.coords[:])))
                                        for l in range(0, len(segs)):
                                            vec0 = [segs[l].coords[1][0] - segs[l].coords[0][0],
                                                    segs[l].coords[1][1] - segs[l].coords[0][1]]
                                            vec1 = [segs[(l + 1) % len(segs)].coords[1][0] -
                                                    segs[(l + 1) % len(segs)].coords[0][0],
                                                    segs[(l + 1) % len(segs)].coords[1][1] -
                                                    segs[(l + 1) % len(segs)].coords[0][1]]
                                            len_vec0 = math.sqrt(vec0[0] ** 2 + vec0[1] ** 2)
                                            len_vec1 = math.sqrt(vec1[0] ** 2 + vec1[1] ** 2)
                                            cos = (vec0[0] * vec1[0] + vec0[1] * vec1[1]) / len_vec0 / len_vec1
                                            if cos <= 0:
                                                print("island seg cos < 0")
                                                break
                                        else:
                                            flag = True
                                            break

                except:
                    pass
            if iters < 10000:
                self.subislands.append(island)

        isles = []
        for i in self.subislands:
            isle = Island(i,world,self)
            isles.append(isle)
            world.ISLANDS.append(isle)
        world.ISLANDS.append(ArchIsland(self.island, world, self, isles))

    def plot(self):
        super().plot()
        plt.plot(*self.poly.exterior.xy, ':r')
        plt.plot(self.x, self.y, 'dr')
        # plt.plot(*self.island.exterior.xy, '-k')
        # for p in self.subislands:
        #     plt.plot(*p.exterior.xy, '-k')
