from generator.Islands.Island import Island
from generator.Structures.BaseCity import BaseCity
from generator.functions import *


class BaseIsland(Island):
    town_area_cof = 0.02

    # def generate1(self):
    #     pass
    def generate(self):
        super().generate()
        sps = []
        for seg in polysegs(self.poly):
            sp = BaseCity(self, seg)
            if sp.is_valid():
                sps.append(sp)
        sps.sort(key=BaseCity.key)
        self.city = sps[0]
        self.city.build()
        for crd in self.city.road_c_points:
            self.road_points.append((crd[0], crd[1]))

    def plot(self):
        super().plot()
        self.city.plot()

    def save(self, data):
        super().save(data)
        self.city.save(data)
