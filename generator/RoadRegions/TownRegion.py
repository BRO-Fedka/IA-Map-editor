from generator.RoadRegions.RoadRegion import RoadRegion
from generator.functions import *
from generator.Structures.SimpleHouse import SimpleHouse



class TownRegion(RoadRegion):
    len_cof = 0

    def __init__(self, poly, island):
        super().__init__(poly, island)
        self.color = "#888"
        self.island.TOWN_RR_AREA.append(poly)

    def generate(self):
        super().generate()
        for edge in self.edges:
            self.island.roads_protos.append(edge)
        if hasattr(self.island, 'sea_port') and self.island.sea_port or hasattr(self.island, 'city'):
            foundation = None
            if hasattr(self.island, 'city'):
                foundation = self.island.city.sp_foundation
            else:
                foundation = self.island.sea_port.sp_foundation
            try:
                sppnt = None
                for p in self.island.road_graf.nodes:
                    if Point(*p).intersects(foundation):
                        if len(list(self.island.road_graf.neighbors(p))) == 1:
                            sppnt = p

                pth = nx.dijkstra_path(self.island.road_graf, self.edges[0][0], sppnt, weight='length')
                self.island.roads_protos.append(pth)
                for i in range(0, len(pth) - 1):
                    self.island.road_graf.remove_edge(pth[i], pth[i + 1])
                    self.island.road_graf.add_edge(pth[i], pth[i + 1], length=0)
                self.island.road_graf.update(self.island.road_graf.edges, self.island.road_graf.nodes)
            except:
                print("NO edges", self.edges)
            # print("PATH SP->BRIDGE", self.roads_protos[-1])

        if len(self.island.bridge_points) > 1:
            for bp in range(0, len(self.island.bridge_points) - 1):
                try:
                    tbp = None
                    for rp in self.island.road_graf.nodes:
                        # print()
                        if Point(*rp).buffer(0.0003).intersects(Point(*self.island.bridge_points[bp])):
                            print('SUC', rp, self.island.bridge_points[bp])
                            tbp = rp
                    pth = nx.dijkstra_path(self.island.road_graf, self.edges[0][0], tbp, weight='length')
                    self.island.roads_protos.append(pth)
                    for i in range(0, len(pth) - 1):
                        self.island.road_graf.remove_edge(pth[i], pth[i + 1])
                        self.island.road_graf.add_edge(pth[i], pth[i + 1], length=0)
                    self.island.road_graf.update(self.island.road_graf.edges, self.island.road_graf.nodes)
                except:
                    print("NO edges",self.edges)
        tedges = polysegs(self.poly)
        tedges = list(map(lambda e: e.coords[:], tedges))
        for i in range(0, 20):
            # print('SH ITER',i,len(tedges))

            for edge in tedges:
                iter = 100
                while iter > 0:
                    iter -= 1
                    h = SimpleHouse(self, edge, 2,0)
                    if h.is_valid():
                        h.build()
                        self.objects.append(h)
                        self.houses.append(h)
                        iter = 0
        # for i in range(0,10):
        #     iter = 1000
        #     while iter > 0:
        #         iter -= 1
        #         h = Well(self)
        #         if h.is_valid():
        #             h.build()
        #             self.objects.append(h)
        #             iter = 0


