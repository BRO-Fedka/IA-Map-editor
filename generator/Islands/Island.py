from generator.functions import *
from shapely.ops import nearest_points
import networkx as nx
from generator.RoadRegions.WoodRegion import WoodRegion
from generator.RoadRegions.TownRegion import TownRegion
from generator.RoadRegions.IndustrialRegion import IndustrialRegion

ISLES_CNT = 0


class Island:
    cnt = 0
    town_area_cof = 0.2
    farm_area_cof = 0  # 0.1

    def __init__(self, poly: Polygon, world, zone, children=None):
        global ISLES_CNT
        self.id = ISLES_CNT
        ISLES_CNT += 1
        self.world = world
        self.poly = poly
        self.zone = zone
        self.bridge_points: List[Tuple] = []
        self.lawn = None
        self.road_zone = None
        self.subislands = children
        self.road_points = []
        self.road_reg_polys = []
        self.markedges = []
        self.markpolys = []
        self.road_regions = []
        self.road_graf: nx.Graph = None
        self.roads_protos = []
        # self.road_lines = []
        self.BUILT_AREA = []
        self.CITY_AREA = []
        self.TOWN_RR_AREA = []
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
            self.road_zone = self.lawn.buffer(-0.1 / self.world.WH)

    def generate1(self):

        flag0 = False

        iters = 50
        for i in self.world.ISLANDS:
            if self != i and self.poly.distance(i.poly) <= 0.75 / self.world.WH:
                pnt, n = nearest_points(self.road_zone, i.poly)
                vec_x = n.x - pnt.x
                vec_y = n.y - pnt.y
                vec_l = math.sqrt(vec_x ** 2 + vec_y ** 2)
                vec_x /= vec_l
                vec_y /= vec_l
                vec_x, vec_y = vec_y, -vec_x
                self.road_points.append((pnt.x + vec_x * 0.00001, pnt.y + vec_y * 0.00001))
                self.road_points.append((pnt.x - vec_x * 0.00001, pnt.y - vec_y * 0.00001))
                self.bridge_points.append((pnt.x, pnt.y))
                # self.bridge_points.append((pnt.x - vec_x * 0.00001, pnt.y - vec_y * 0.00001))
                # self.BUILT_AREA.append(
                #     Point(pnt.x + vec_x * 0.00001, pnt.y + vec_y * 0.00001).buffer(0.125 / self.world.WH))
                # self.BUILT_AREA.append(
                #     Point(pnt.x - vec_x * 0.00001, pnt.y - vec_y * 0.00001).buffer(0.125 / self.world.WH))
        n = math.ceil(self.poly.area / (0.025 * 0.025))
        print(self.id, "RR per ISLE", n)
        # n = max(n, 3)
        bu_road_points = self.road_points.copy()
        bu_BA = self.BUILT_AREA.copy()
        print('flag0')
        while not flag0 and iters > 0:  # and iters > 0
            iters -= 1

            # if len(self.road_points) > 2 and not hasattr(self, 'sea_port'):  # and not hasattr(self, 'seaport')
            #
            #     n = 0
            self.road_points = bu_road_points.copy()
            self.BUILT_AREA = bu_BA.copy()
            lv_here = False
            for _ in range(0, n):
                flag = False
                itr = 200
                while not flag and itr > 0:
                    itr -= 1
                    x = self.poly.bounds[0] + (self.poly.bounds[2] - self.poly.bounds[0]) * random()
                    y = self.poly.bounds[1] + (self.poly.bounds[3] - self.poly.bounds[1]) * random()
                    p = Point(x, y)
                    if p.intersects(self.poly.buffer(-0.125 / 2 / self.world.WH)):
                        for sh in self.BUILT_AREA + self.CITY_AREA:  # +self.ROAD_BLOCK_AREA
                            f = sh.buffer(0.125 * 1.5 / self.world.WH)  # 0.25
                            # plt.plot(*f.exterior.xy, '-r')
                            if p.intersects(f):
                                break
                        else:
                            flag = True
                            self.road_points.append((x, y))
                            # self.BUILT_AREA.append(Point(x, y).buffer(0.125 / 2 / self.world.WH))  # 0.125
                if itr <= 0:
                    lv_here = True
            if lv_here:
                flag0 = True
                continue

            base_points = MultiPoint(self.road_points)
            rr = voronoi_diagram(base_points, self.poly)
            lslawn = LineString([*self.road_zone.exterior.coords[:]] + [self.road_zone.exterior.coords[0]])
            Lslawn = lslawn.buffer(0.0000001)
            crds: Dict[Tuple, Set[Tuple]] = {}
            self.road_reg_polys = []
            for r in rr:
                try:
                    z = r.intersection(self.road_zone)
                    # if type(z) == GeometryCollection:
                    #     flag0 = True
                    #     break
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

                    self.road_reg_polys.append(z)
                except:
                    pass
            # if flag0: continue
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
                    self.road_graf.add_edge(_, __, length=Point(*_).distance(Point(*__)))
            # print('GRAPH',nx.is_connected(self.road_graf))
            # nx.is_
            # print(self.road_graf.edges)
            print("GEN R", self.id)
            try:
                if not nx.is_connected(self.road_graf):
                    print(self.id, "Rgraf unconnected")
                    # nx.draw_spring(self.road_graf)
                    # plt.show()
                    continue
                else:
                    pass
            except:
                print(self.id, "Rgraf null")
                continue
            try:
                if len(crds.keys()) < len(rr) + 1:
                    print('To less R nodes')
                    continue
            except:
                continue
            self.road_reg_polys.sort(key=lambda e: e.area)
            area_town_left = self.town_area_cof * self.poly.area
            area_farm_left = self.farm_area_cof * self.poly.area
            industrials = 5
            for rp in self.road_reg_polys:
                city = False
                for sh in self.CITY_AREA:
                    if rp.intersects(sh):
                        city = True
                sp_dst_wh = self.world.WH / 2
                if hasattr(self, 'sea_port') and self.sea_port:
                    sp_dst_wh = rp.distance(self.sea_port.sp_foundation) * self.world.WH
                if hasattr(self, 'city') and self.city:
                    sp_dst_wh = rp.distance(self.city.sp_foundation) * self.world.WH
                # if

                area_wh = rp.area * self.world.WH ** 2
                rectness = rp.area / rp.minimum_rotated_rectangle.area
                if (area_wh / (0.16 * 0.16)) * rectness ** 2 <= 1:
                    self.road_regions.append(WoodRegion(rp, self))
                    continue
                if rp.area < area_town_left or city:
                    if True:
                        area_town_left -= rp.area
                        if city and area_wh > 0.7 * 0.7 and rectness > 0.99 and sp_dst_wh > 0 and industrials > 0:
                            self.road_regions.append(IndustrialRegion(rp, self))
                            industrials -= 1
                        else:
                            self.road_regions.append(TownRegion(rp, self))
                # elif rp.area < area_farm_left and sp_dst_wh > 0:
                #     if True:
                #         area_farm_left -= rp.area
                #         self.road_regions.append(FarmRegion(rp, self))
                # if (area_wh < 0.33) or (
                #         sp_dst_wh <= 0 and area_wh <= 1.5 and rectness > 0.85):
                #     self.road_regions.append(TownRegion(rp, self))
                else:
                    self.road_regions.append(WoodRegion(rp, self))
            for rr in self.road_regions:
                rr.generate()
            self.bridge_points = list(set(self.bridge_points))
            if hasattr(self, 'sea_port') and self.sea_port:

                sppnt = None
                for p in self.road_graf.nodes:
                    if Point(*p).intersects(self.sea_port.sp_foundation):
                        if len(list(self.road_graf.neighbors(p))) == 1:
                            sppnt = p
                pths = []
                for bp in self.bridge_points:
                    tbp = None
                    for rp in self.road_graf.nodes:
                        # print()
                        if Point(*rp).buffer(0.0003).intersects(Point(*bp)):
                            print('SUC', rp, bp)
                            tbp = rp
                            break
                    # print(self.road_graf.has_node(tbp))
                    # print(self.road_graf.has_node(sppnt))
                    # if tbp is None:
                    #     continue
                    pths.append([nx.dijkstra_path_length(self.road_graf, tbp, sppnt, weight='length'), tbp])
                pths.sort(key=lambda e: e[0])
                for bp in pths:
                    print(self.id, "BUILD ROAD", bp)
                    pth = nx.dijkstra_path(self.road_graf, bp[1], sppnt, weight='length')
                    self.roads_protos.append(pth)
                    for i in range(0, len(pth) - 1):
                        self.road_graf.remove_edge(pth[i], pth[i + 1])
                        self.road_graf.add_edge(pth[i], pth[i + 1], length=0)
                    self.road_graf.update(self.road_graf.edges, self.road_graf.nodes)

                    # print("PATH SP->BRIDGE", self.roads_protos[-1])
            print(0)
            if len(self.bridge_points) > 1:
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
                        pth = nx.dijkstra_path(self.road_graf, tbp0, tbp1, weight='length')
                        self.roads_protos.append(pth)
                        for i in range(0, len(pth) - 1):
                            self.road_graf.remove_edge(pth[i], pth[i + 1])
                            self.road_graf.add_edge(pth[i], pth[i + 1], length=0)
                        self.road_graf.update(self.road_graf.edges, self.road_graf.nodes)
                        # print(nx.shortest_path_length(self.road_graf, tbp0, tbp1, "bell-ford"))
                        print("PATH SP->BRIDGE", self.roads_protos[-1])
                    except:
                        pass
                print(1)

            else:
                pass
            # pos = nx.planar_layout(self.road_graf)
            # nx.draw(self.road_graf, pos)
            # nx.draw_networkx_edge_labels(self.road_graf, pos)
            # plt.show()

            print(2)
            # self.road_lines.append(LinearRing(r.coords).intersection(self.lawn))

            print(3)

            flag0 = True
        print("ITERS", iters)

    def generate2(self):
        pass

    def save(self, data):
        if not "B" in data.keys():
            data["B"] = []
        data["B"].append(
            list(map(lambda v: list(map(lambda g: round(g * self.world.WH, 2), v)), self.poly.exterior.coords[:])))
        if not "G" in data.keys():
            data["G"] = []
        try:
            data["G"].append(
                list(map(lambda v: list(map(lambda g: round(g * self.world.WH, 2), v)), self.lawn.exterior.coords[:])))
        except:
            pass
        for rr in self.road_regions:
            rr.save(data)
        all_roads = set()
        for r in self.roads_protos:
            seq = tuple(map(tuple,r))
            for i in range(0,len(seq)-1):
                all_roads.add(((round(seq[i][0] * self.world.WH, 2),round(seq[i][1] * self.world.WH, 2)), (round(seq[i+1][0] * self.world.WH, 2),round(seq[i+1][1] * self.world.WH, 2))))
                # l = LineString((seq[i],seq[i+1]))
                # for sh in self.BUILT_AREA:
                #     if l.intersects(sh):
                #         break
                # else:
                #     all_roads.add((seq[i], seq[i + 1]))

                # try:
                #     l = LineString((seq[i],seq[i+1]))
                #     s = []
                #     for sh in self.BUILT_AREA:
                #         if l.intersects(sh):
                #             nl = l.difference(sh)
                #             s = tuple(map(tuple, nl.coords[:]))
                #             break
                #     else:
                #         s = (seq[i], seq[i + 1])
                #     all_roads.add((seq[i],seq[i+1]))
                # except:pass

        if len(all_roads) > 0:
            if not 'R' in data:
                data['R'] = []
            for r in list(all_roads):
                if r[0] != r[1]:
                    data['R'].append(list(map(list,r)))

    def plot(self):
        plt.plot(*self.poly.exterior.xy, '-k')
        # plt.plot(*self.road_zone.exterior.xy, '-r')

        # plt.plot(self.aver_center.x, self.aver_center.y, 'xm')
        plt.plot(self.poly.centroid.x, self.poly.centroid.y, 'xy')
        # self.road_t_points = list(self.road_t_points)
        if self.lawn:
            plt.plot(*self.lawn.exterior.xy, '-g')
        for r in self.road_reg_polys:
            plt.plot(*r.exterior.xy, '-y')
        for r in self.road_points:
            plt.plot(r[0], r[1], '.g')
        # i

        # plt.text(self.poly.centroid.x, self.poly.centroid.y, str(self.id))
        if self.road_graf:
            for r in self.road_graf.edges:
                plt.plot(*LineString([r[0], r[1]]).xy, '-m')
        # if self.roads_protos:
        for rr in self.road_regions:
            rr.plot()
        # for r in self.roads_protos:
        #     try:
        #         plt.plot(*LineString(r).xy, '-k')
        #     except:
        #         pass
        for r in self.markedges:
            plt.plot(*LineString([r[0], r[1]]).xy, '-r')
        # for r in self.BUILT_AREA:
        #     plt.plot(*r.exterior.xy, '-m')
        
