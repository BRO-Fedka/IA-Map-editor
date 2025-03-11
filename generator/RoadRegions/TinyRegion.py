from generator.RoadRegions.RoadRegion import RoadRegion


class TinyRegion(RoadRegion):
    def __init__(self, poly, island):
        super().__init__(poly,island)
        self.color = "#f00"
