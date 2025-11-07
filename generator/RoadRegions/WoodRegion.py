from generator.RoadRegions.RoadRegion import RoadRegion
from generator.functions import *
from generator.Structures.SimpleHouse import SimpleHouse
from generator.Structures.Rock import Rock
from generator.Structures.Tree import Tree


class WoodRegion(RoadRegion):
    def __init__(self, poly, island):
        super().__init__(poly, island)
        self.color = "#080"

    def generate(self):
        super().generate()
        town_edges = []
        for sh in self.island.TOWN_RR_AREA:
            if self.poly.intersects(sh):
                print('LOOOOL')
                for edge in self.edges:
                    if Point(*edge[0]).intersects(sh) and Point(*edge[1]).intersects(sh):
                        town_edges.append(edge)
                        # self.island.markedges.append(edge)
                        for i in range(0, 5):
                            iter = 1#randint(20, 30)
                            while iter > 0:
                                iter -= 1
                                h = SimpleHouse(self, edge)
                                if h.is_valid():
                                    h.build()
                                    self.objects.append(h)
                                    self.houses.append(h)
                                    break
        for _ in range(0, randint(1, 5) ** 2):
            iter = 1#50#100
            while iter > 0:
                iter -= 1
                h = Rock(self)
                if h.is_valid():
                    h.build()
                    self.objects.append(h)
                    break
        for _ in range(0,randint(2, 8) ** 2):
            iter = 1#2
            while iter > 0:
                iter -= 1
                h = Tree(self)
                if h.is_valid():
                    h.build()
                    self.trees.append(h)
                    break
