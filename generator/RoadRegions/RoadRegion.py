from generator.functions import *


# nx.cond
class RoadRegion:
    len_cof = 1

    def __init__(self, poly, island):
        self.objects = []
        self.poly = poly
        self.island = island
        self.ROCK_AREAS = []
        self.TREE_POINTS = []
        self.TREE_AREAS = []
        self.houses = []
        self.trees = []

        self.color = "#fff"
        self.roaded_points = set()
        self.edges = []
        for edge in self.island.road_graf.edges:
            if Point(*edge[0]).intersects(self.poly) and Point(*edge[1]).intersects(self.poly):
                self.roaded_points.add(edge[0])
                self.roaded_points.add(edge[1])
                length = self.island.road_graf.get_edge_data(*edge)['length']
                self.island.road_graf.remove_edge(*edge)
                self.island.road_graf.add_edge(*edge, length=length * self.len_cof)
                self.edges.append(edge)

            # print(edge, type(edge), dir(edge))
        self.island.road_graf.update(self.island.road_graf.edges, self.island.road_graf.nodes)

    def save(self, data):
        for obj in self.objects:
            try:
                obj.save(data)
            except:
                pass
        hlist = []
        for h in self.houses:
            h.save(hlist)
        if not '#' in data.keys():
            data['#'] = []
        if len(hlist) > 0:
            data['#'].append(hlist)
        htrees = []
        for h in self.trees:
            h.save(htrees)
        if not 'T' in data.keys():
            data['T'] = []
        if len(htrees) > 0:
            data['T'].append(htrees)

    def generate(self):
        pass

    def plot(self):
        plt.fill(*self.poly.exterior.xy, facecolor=self.color, edgecolor='none')
        for obj in self.objects:
            obj.plot()
            print(type(self))
