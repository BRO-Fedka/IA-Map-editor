from generator.Zones import *
import json
from perlin_noise import PerlinNoise


class WorldCommon:
    def __init__(self, sd, wh=32):
        seed(sd)
        self.MAP_SQUARE = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
        self.MAP_SQUARE_LS = LineString([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])
        self.ZONES = []
        self.BASES = []
        self.AREAS = []
        self.RATIOS = []
        self.ISLANDS = []
        self.BUILT_AREA = []
        self.TREETYPE_NOISE = PerlinNoise(octaves=30, seed=sd)
        self.BRIDGES = []
        self.WH = wh


def generate(s, wh=32):
    # input()
    world = WorldCommon(s, wh)
    Island.cnt = 0

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
            world.RATIOS.append(
                z)  # max((z.poly.bounds[3] - z.poly.bounds[1]) / (z.poly.bounds[2] - z.poly.bounds[0]),(z.poly.bounds[2] - z.poly.bounds[0]) / (z.poly.bounds[3] - z.poly.bounds[1]))
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
    # for i in world.ISLANDS:
    #     i.generate2()

    for z in world.ZONES:
        z.plot()
    for i in world.ISLANDS:
        i.plot()

    ax = plt.gca()
    ax.set_xticks(numpy.arange(0, 1, 1 / world.WH))
    ax.set_yticks(numpy.arange(0, 1., 1 / world.WH))

    plt.grid(True)
    plt.show()
    print('FINISH')
    # input()
    data = {}
    with open('template.json') as f:
        data = json.loads(f.read())
    for i in world.ISLANDS:
        i.save(data)
    with open(f'maps/MAP{s}.json','w') as f:
        f.write(json.dumps(data))
    return True


if __name__ == "__main__":
    flag = False
    i = 12
    seeds = []
    exceptions = []
    # 12
    # TODO 158 BRIDGES
    # TODO 367 OMG wtf
    # 554
    # 675
    # 835
    f = open('seeds.txt', 'w')
    f.write('')
    f.close()
    f = open('exceptions.txt', 'w')
    f.write('')
    f.close()
    while not flag:
        # try:
        flag = generate(i)
        # except:
        #     exceptions.append(i)
        #     with open('exceptions.txt','w') as f:
        #         for _ in exceptions:
        #             f.write('\n'+str(_))
        if flag:
            seeds.append(i)

            with open('seeds.txt', 'w') as f:
                for _ in seeds:
                    f.write('\n' + str(_))

        i += 1
        flag = False
