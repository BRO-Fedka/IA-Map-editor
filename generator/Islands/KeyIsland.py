from generator.Islands.Island import Island
from generator.functions import *
from generator.Structures.KeySeaPort import KeySeaPort


class KeyIsland(Island):
    def __init__(self, poly: Polygon, world, zone, children=None):
        super().__init__(poly, world, zone, children)
        self.sea_port = None

    def generate(self):
        super().generate()
        if self.poly.area <= 0.075 * 0.075:
            print('isles too small')
            return

        sps = []
        for seg in polysegs(self.poly):
            sp = KeySeaPort(self, seg)
            if sp.is_valid():
                sps.append(sp)
        if len(sps) == 0:
            for seg in polysegs(self.poly):
                sp = KeySeaPort(self, seg, no_pier=True)
                if sp.is_valid():
                    sps.append(sp)
        sps.sort(key=KeySeaPort.key)
        self.sea_port = sps[0]
        self.sea_port.build()
        for crd in self.sea_port.sp_foundation.exterior.coords:
            self.road_points.append((crd[0], crd[1]))

    def generate1(self):
        super().generate1()


    def plot(self):
        super().plot()
        all_ises = self.subislands + [self]
        sx = 0
        sy = 0
        asx = 0
        asy = 0
        sasx = 1
        sasy = 1
        for _ in all_ises:
            asx += _.aver_center.x
            asy += _.aver_center.y
            sasx *= _.aver_center.x
            sasy *= _.aver_center.y
            sx += _.poly.centroid.x
            sy += _.poly.centroid.y
        sx /= len(all_ises)
        sy /= len(all_ises)
        asx /= len(all_ises)
        asy /= len(all_ises)
        sasx **= 1 / len(all_ises)
        sasy **= 1 / len(all_ises)
        plt.plot(asx, asy, '.m')
        plt.plot(sx, sy, '.y')
        plt.plot(sasx, sasy, 'xg')
        if self.sea_port:
            self.sea_port.plot()

