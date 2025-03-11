from generator.RoadRegions.TownRegion import TownRegion


class IndustrialRegion(TownRegion):
    def __init__(self, poly, island):
        super().__init__(poly,island)
        self.color = "#444"
