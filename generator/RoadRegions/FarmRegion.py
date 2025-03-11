from generator.RoadRegions.RoadRegion import RoadRegion


class FarmRegion(RoadRegion):
    len_cof = 0.75

    def __init__(self, poly, island):
        super().__init__(poly, island)
        self.color = "#ff0"
