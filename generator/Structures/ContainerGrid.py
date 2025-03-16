from generator.functions import *


class ContainerGrid:
    def __init__(self, poly, island):
        self.poly = poly
        # print(poly)
        segs = polysegs(poly)
        # print(segs)
        row = (segs[0].length * island.world.WH) // 0.1
        column = (segs[1].length * island.world.WH) // 0.05
        orig = segs[0].coords[0]
        vec_x = (segs[0].coords[1][0] - segs[0].coords[0][0], segs[0].coords[1][1] - segs[0].coords[0][1])
        vec_y = (segs[1].coords[1][0] - segs[1].coords[0][0], segs[1].coords[1][1] - segs[1].coords[0][1])
        deg = lookat(*vec_x)
        self.containers = []
        for x in range(0, int(row)):
            for y in range(0, int(column)):
                xcof = (x * 0.1 + 0.05) / island.world.WH / segs[0].length
                ycof = (y * 0.05 + 0.025) / island.world.WH / segs[1].length
                if (x == 0 or x == row - 1 or y == 0 or y == column - 1) and random() > 0.8:
                    continue

                self.containers.append([1, round((orig[0] + vec_x[0] * xcof + vec_y[0] * ycof) * island.world.WH, 2),
                                        round((orig[1] + vec_x[1] * xcof + vec_y[1] * ycof) * island.world.WH, 2), 0.05,
                                        0.1, round((deg + 90) % 360)])

    def get_as_list(self):
        return self.containers
