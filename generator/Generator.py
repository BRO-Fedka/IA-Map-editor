from generator.Zones import *


class WorldCommon:
    def __init__(self, sd, wh=32):
        seed(sd)
        self.MAP_SQUARE = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        self.ZONES = []
        self.BASES = []
        self.AREAS = []
        self.RATIOS = []
        self.ISLANDS = []
        self.BUILT_AREA = []
        self.BRIDGES = []
        self.WH = wh


def generate(s,wh=32):
    world = WorldCommon(s,wh)

    points = [(0.1, 0.1), (0.9, 0.9)]

    for _ in range(0, 12):
        while True:
            x = random()
            y = random()
            dst = x + y
            if ((1 - abs(1 - dst)) ** 2) > random():  # ((1 - abs(1 - dst)) ** 2) > random()
                points.append((x, y))
                break
        # print(points)
    base_points = MultiPoint(points)
    regions = voronoi_diagram(base_points)
    regions = list(map(lambda p: p.intersection(world.MAP_SQUARE), regions.geoms))
    for p in points:
        for r in regions:
            if Point(p).intersects(r):
                world.ZONES.append(Zone(p[0], p[1], r, world))
                break

    for _ in range(0, len(world.ZONES) + 1):
        for z in world.ZONES:
            z.generate(0, world)

    for z in world.ZONES:
        if type(z) == Zone:
            world.AREAS.append(z)  # z.poly.area
            world.RATIOS.append(z)  # max((z.poly.bounds[3] - z.poly.bounds[1]) / (z.poly.bounds[2] - z.poly.bounds[0]),(z.poly.bounds[2] - z.poly.bounds[0]) / (z.poly.bounds[3] - z.poly.bounds[1]))
    world.AREAS.sort(key=lambda z: z.poly.area)
    world.RATIOS.sort(key=lambda z: z.ratio)
    if world.AREAS[0].poly.area < 0.1 * 0.1:
        print('zone area')
        return False
    if world.RATIOS[-1].ratio > 1.75:
        print('zone ratio')
        return False

    for stage in range(1, 10):
        for _ in range(0, len(world.ZONES) + 1):
            for z in world.ZONES:
                z.generate(stage, world)
    for z in world.ZONES:
        if z.poly.area / ((z.poly.bounds[3] - z.poly.bounds[1]) * (z.poly.bounds[2] - z.poly.bounds[0])) < 0.4:
            print('zone rel area')
            return False
    if world.BASES[0].poly.area / ((world.BASES[0].poly.bounds[3] - world.BASES[0].poly.bounds[1]) * (
            world.BASES[0].poly.bounds[2] - world.BASES[0].poly.bounds[0])) < 0.6 or world.BASES[1].poly.area / (
            (world.BASES[1].poly.bounds[3] - world.BASES[1].poly.bounds[1]) * (
            world.BASES[1].poly.bounds[2] - world.BASES[1].poly.bounds[0])) < 0.6:
        print('base rel area')
        return False

    if max(world.BASES[0].poly.area / world.BASES[1].poly.area,
           world.BASES[1].poly.area / world.BASES[0].poly.area) > 1.25:
        print('base area ratio')
        return False
    plt.figure()
    for i in world.ISLANDS:
        i.generate()
    for i in world.ISLANDS:
        i.generate1()
    for i in world.ISLANDS:
        i.generate2()

    for z in world.ZONES:
        z.plot()
    for i in world.ISLANDS:
        i.plot()

    # print(BASES[0].poly.bounds)
    # print(BASES[1].poly.bounds)

    # print(ZONES)
    ax = plt.gca()
    ax.set_xticks(numpy.arange(0, 1, 1 / world.WH))
    ax.set_yticks(numpy.arange(0, 1., 1 / world.WH))

    plt.grid(True)
    plt.show()
    return True


if __name__ == "__main__":
    flag = False
    i = 12
    # TODO 158 BRIDGES
    while not flag:
        flag = generate(i)
        if flag:
            print(i)
        i += 1
        flag = False
