from generator.functions import *
from shapely.ops import nearest_points
import networkx as nx


class Island:
    cnt = 0

    def __init__(self, poly: Polygon, world, zone, children=None):
        self.id = self.__class__.cnt
        self.__class__.cnt += 1
        self.world = world
        self.poly = poly
        self.zone = zone
        self.bridge_points: List[Tuple] = []
        self.lawn = None
        self.subislands = children
        self.road_points = []
        self.road_regions = []
        self.road_graf = None
        self.roads_protos = []
        # self.road_lines = []
        self.BUILT_AREA = []
        self.road_graf_points = []
        # self.road_t_points = set()
        sx = 0
        sy = 0
        for _ in self.poly.exterior.coords:
            sx += _[0]
            sy += _[1]
        self.aver_center = Point(sx / len(self.poly.exterior.coords), sy / len(self.poly.exterior.coords))
        if children is None:
            self.subislands = []

    def generate(self):
        if self.poly.area > (0.75 / self.world.WH) ** 2:
            self.lawn = self.poly.buffer(-0.1 / self.world.WH)

    def generate1(self):

        flag0 = False

        # iters = 50
        for i in self.world.ISLANDS:
            if self != i and self.poly.distance(i.poly) <= 0.75 / self.world.WH:
                pnt, n = nearest_points(self.poly.buffer(-0.1 / self.world.WH), i.poly)
                vec_x = n.x - pnt.x
                vec_y = n.y - pnt.y
                vec_l = math.sqrt(vec_x ** 2 + vec_y ** 2)
                vec_x /= vec_l
                vec_y /= vec_l
                vec_x, vec_y = vec_y, -vec_x
                self.road_points.append((pnt.x + vec_x * 0.00001, pnt.y + vec_y * 0.00001))
                self.road_points.append((pnt.x - vec_x * 0.00001, pnt.y - vec_y * 0.00001))
                self.bridge_points.append((pnt.x + vec_x * 0.00001, pnt.y + vec_y * 0.00001))
                self.bridge_points.append((pnt.x - vec_x * 0.00001, pnt.y - vec_y * 0.00001))
                self.BUILT_AREA.append(
                    Point(pnt.x + vec_x * 0.00001, pnt.y + vec_y * 0.00001).buffer(0.125 / self.world.WH))
                self.BUILT_AREA.append(
                    Point(pnt.x - vec_x * 0.00001, pnt.y - vec_y * 0.00001).buffer(0.125 / self.world.WH))
        n = round(self.poly.area / (0.025 * 0.05))
        n = max(n, 3)
        bu_road_points = self.road_points.copy()
        bu_BA = self.BUILT_AREA.copy()

        while not flag0:  # and iters > 0
            # iters -= 1

            # if len(self.road_points) > 2 and not hasattr(self, 'sea_port'):  # and not hasattr(self, 'seaport')
            #
            #     n = 0
            self.road_points = bu_road_points
            self.BUILT_AREA = bu_BA
            for _ in range(0, n):
                flag = False
                while not flag:
                    x = self.poly.bounds[0] + (self.poly.bounds[2] - self.poly.bounds[0]) * random()
                    y = self.poly.bounds[1] + (self.poly.bounds[3] - self.poly.bounds[1]) * random()
                    p = Point(x, y)
                    if p.intersects(self.poly):
                        for sh in self.BUILT_AREA:
                            f = sh.buffer(0.25 / self.world.WH)
                            # plt.plot(*f.exterior.xy, '-r')
                            if p.intersects(f):
                                break
                        else:
                            flag = True
                            self.road_points.append((x, y))
                            self.BUILT_AREA.append(Point(x, y).buffer(0.125 / self.world.WH))

            base_points = MultiPoint(self.road_points)
            rr = voronoi_diagram(base_points, self.poly)
            lslawn = LineString([*self.lawn.exterior.coords[:]] + [self.lawn.exterior.coords[0]])
            Lslawn = lslawn.buffer(0.0000001)
            crds: Dict[Tuple, Set[Tuple]] = {}
            self.road_regions = []
            for r in rr:
                z = r.intersection(self.lawn)
                if type(z) == GeometryCollection:
                    flag0 = True
                    break
                if z.intersects(lslawn):
                    # bds = z.intersection(lslawn)
                    lstcrds = [z.exterior.coords[-1]] + [*z.exterior.coords[:]] + [z.exterior.coords[0]]
                    for i in range(0, len(lstcrds) - 2):
                        if not Point(*lstcrds[i + 1]).intersects(Lslawn):
                            if not lstcrds[i + 1] in crds.keys():
                                crds[lstcrds[i + 1]] = set()
                            crds[lstcrds[i + 1]].add(lstcrds[i])
                            crds[lstcrds[i + 1]].add(lstcrds[i + 2])
                            if not lstcrds[i + 2] in crds.keys():
                                crds[lstcrds[i + 2]] = set()
                            crds[lstcrds[i + 2]].add(lstcrds[i + 1])
                            if not lstcrds[i] in crds.keys():
                                crds[lstcrds[i]] = set()
                            crds[lstcrds[i]].add(lstcrds[i + 1])


                else:
                    lstcrds = [z.exterior.coords[-1]] + [*z.exterior.coords[:]] + [z.exterior.coords[0]]
                    for i in range(0, len(lstcrds) - 2):
                        if not lstcrds[i + 1] in crds.keys():
                            crds[lstcrds[i + 1]] = set()
                        crds[lstcrds[i + 1]].add(lstcrds[i])
                        crds[lstcrds[i + 1]].add(lstcrds[i + 2])

                self.road_regions.append(z)
            if flag0: continue
            for _ in crds.keys():
                for __ in list(crds[_]):
                    if not __ in crds.keys():
                        crds[_].remove(__)
                    if __ == _:
                        crds[_].remove(__)
                    # self.road_t_points.add(__)
            # print(crds)
            self.road_graf_points = []
            self.road_graf = nx.Graph()
            # self.road_graf.
            for _ in crds.keys():
                self.road_graf_points.append(Point(*_))
                self.road_graf.add_node(_)
                for __ in list(crds[_]):
                    self.road_graf.add_edge(_, __, length=Point(*_).distance(Point(*__)),
                                            weight=Point(*_).distance(Point(*__)))
            # print('GRAPH',nx.is_connected(self.road_graf))
            # nx.is_
            # print(self.road_graf.edges)
            print("GEN R", self.id)
            if not nx.is_connected(self.road_graf):
                print(self.id, "Rgraf unconnected")
                # nx.draw_spring(self.road_graf)
                # plt.show()
                continue
            else:
                pass
            if hasattr(self, 'sea_port') and self.sea_port:
                sppnt = None
                for p in self.road_graf.nodes:
                    if Point(*p).intersects(self.sea_port.sp_foundation):
                        if len(list(self.road_graf.neighbors(p))) == 1:
                            sppnt = p
                for bp in self.bridge_points:
                    tbp = None
                    for rp in self.road_graf.nodes:
                        # print()
                        if Point(*rp).buffer(0.0003).intersects(Point(*bp)):
                            print('SUC', rp, bp)
                            tbp = rp
                    # print(self.road_graf.has_node(tbp))
                    # print(self.road_graf.has_node(sppnt))
                    self.roads_protos.append(nx.shortest_path(self.road_graf, tbp, sppnt))
                    print("PATH SP->BRIDGE", self.roads_protos[-1])
            if len(self.bridge_points) > 0:
                for bp in range(0, len(self.bridge_points) - 1):
                    tbp0 = None
                    tbp1 = None
                    for rp in self.road_graf.nodes:
                        # print()
                        if Point(*rp).buffer(0.0003).intersects(Point(*self.bridge_points[bp])):
                            print('SUC', rp, self.bridge_points[bp])
                            tbp0 = rp
                    for rp in self.road_graf.nodes:
                        # print()
                        if Point(*rp).buffer(0.0003).intersects(Point(*self.bridge_points[bp + 1])):
                            print('SUC', rp, self.bridge_points[bp + 1])
                            tbp1 = rp
                    try:
                        self.roads_protos.append(nx.shortest_path(self.road_graf, tbp0, tbp1))
                        print("PATH SP->BRIDGE", self.roads_protos[-1])
                    except:
                        pass


            else:
                pass
                # self.road_lines.append(LinearRing(r.coords).intersection(self.lawn))
            if len(crds.keys()) < len(rr) + 1:
                continue

            flag0 = True

    def generate2(self):
        pass

    def plot(self):
        plt.plot(*self.poly.exterior.xy, '-k')
        plt.plot(self.aver_center.x, self.aver_center.y, 'xm')
        plt.plot(self.poly.centroid.x, self.poly.centroid.y, 'xy')
        # self.road_t_points = list(self.road_t_points)
        if self.lawn:
            plt.plot(*self.lawn.exterior.xy, '-g')
        for r in self.road_regions:
            plt.plot(*r.exterior.xy, '-y')
        # for r in self.road_t_points:
        #     plt.plot(r[0], r[1], '.g')
        # if
        plt.text(self.poly.centroid.x, self.poly.centroid.y, str(self.id))
        if self.road_graf:
            for r in self.road_graf.edges:
                plt.plot(*LineString([r[0], r[1]]).xy, '--m')
        # if self.roads_protos:
        for r in self.roads_protos:
            try:
                plt.plot(*LineString(r).xy, '-k')
            except:pass