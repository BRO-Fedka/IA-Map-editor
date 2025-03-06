from shapely.geometry import Polygon, LinearRing
import random
import pickle
import logging
# import BFint
import math


def lookat(x, y):
    if x == 0:
        x = 0.001
    angle = math.atan((y / x)) / (math.pi / 180)
    if y != abs(y):
        angle = angle + 360
    if x != abs(x):
        angle = angle + 180
    return angle % 360


def generatePolygon2(p, pix):
    points = []
    cx, cy = 0, 0
    for sim in p:
        cx += sim[0]
        cy += sim[1]
    cx = cx / len(p)
    cy = cy / len(p)
    for _ in range(0, len(p)):
        points.append(p[_])
        d = (math.sqrt((p[int((_ + 1) % len(p))][0] - cx) ** 2 + (p[int((_ + 1) % len(p))][1] - cy) ** 2) + math.sqrt(
            (p[_][0] - cx) ** 2 + (p[_][1] - cy) ** 2)) / 2
        d0 = lookat(p[_][0] - cx, p[_][1] - cy)
        d1 = lookat(p[int((_ + 1) % len(p))][0] - cx, p[int((_ + 1) % len(p))][1] - cy)
        if abs(d0 - d1) > 180:
            if d0 < d1:
                d0 += 360
            else:
                d1 += 360
        d2 = ((d0 + d1) / 2) % 360
        d3 = math.sqrt((p[_][0] - p[int((_ + 1) % len(p))][0]) ** 2 + (p[_][1] - p[int((_ + 1) % len(p))][1]) ** 2) / d
        points.append([cx + math.cos(d2 / 180 * math.pi) * d * d3, cy + math.sin(d2 / 180 * math.pi) * d * d3])
    return points


def generatePolygon(ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts):
    irregularity = clip(irregularity, 0, 1) * 2 * math.pi / numVerts
    spikeyness = clip(spikeyness, 0, 1) * aveRadius
    angleSteps = []
    lower = (2 * math.pi / numVerts) - irregularity
    upper = (2 * math.pi / numVerts) + irregularity
    sum = 0
    for i in range(numVerts):
        tmp = random.uniform(lower, upper)
        angleSteps.append(tmp)
        sum = sum + tmp
    k = sum / (2 * math.pi)
    for i in range(numVerts):
        angleSteps[i] = angleSteps[i] / k
    points = []
    angle = random.uniform(0, 2 * math.pi)
    for i in range(numVerts):
        r_i = clip(random.gauss(aveRadius, spikeyness), 0, 2 * aveRadius)
        x = ctrX + r_i * math.cos(angle)
        y = ctrY + r_i * math.sin(angle)
        points.append((x, y))
        angle = angle + angleSteps[i]
    return points


def clip(x, min, max):
    if (min > max):
        return x
    elif (x < min):
        return min
    elif (x > max):
        return max
    else:
        return x


def smoothPolygon(p, pix):
    points = []
    for _ in range(0, len(p)):
        a0 = p[_][0] + (
                    (((p[(len(p) + _ - 1) % len(p)][0] + p[_][0]) / 2 + (p[(_ + 1) % len(p)][0] + p[_][0]) / 2) / 2) -
                    p[_][0]) * pix
        a1 = p[_][1] + (
                    (((p[(len(p) + _ - 1) % len(p)][1] + p[_][1]) / 2 + (p[(_ + 1) % len(p)][1] + p[_][1]) / 2) / 2) -
                    p[_][1]) * pix
        points.append([a0, a1])
    return points


def main():
    random.seed(0)
    MAP = {'B': [], 'G': [], 'S': [], 'Z': [], 'Q': {}}
    for _ in range(0, 10000):
        try:
            #     deg = random.random() * math.pi*2
            #     dis = 100*random.random()
            generatePolygon()
            poly = generatePolygon(10 + random.random() * 236, 10 + random.random() * 236, random.random() * 5, 0.5,
                                   0.5, random.randint(10, 30))  # 128+math.cos(deg)*dis,128+math.sin(deg)*dis
            poly = generatePolygon2(poly, 0)
            for _ in range(0, 2):
                poly = smoothPolygon(poly, 2)
            for _ in range(0, 2):
                poly = smoothPolygon(poly, 1)
            g = Polygon(poly).area > 2.25
            zone = LinearRing(poly).parallel_offset(1.0, 'right', join_style=2)
            ground = LinearRing(poly).parallel_offset(-0.5, 'right', join_style=2)
            ln = LinearRing(poly)
            poly = Polygon(poly)
            if g and (ground.intersects(ln) or ground.intersects(zone)): continue
            if tuple(zone.coords) == (): continue
            if g and tuple(ground.coords) == (): continue
            if g and ground.area > poly.area: continue
            zone = Polygon(zone.coords)
            if g: ground = Polygon(ground.coords)
            ok = True

            for _0 in MAP['Z']:
                if _0.intersects(poly): ok = False
            if ok:
                MAP['B'].append(poly)
                MAP['Z'].append(zone)
                if g: MAP['G'].append(ground)
        except Exception:
            logging.exception("message")
    for x in range(0, 256):
        for y in range(0, 256):
            MAP['Q'][(x, y)] = {'p': Polygon([[x, y], [x + 1, y], [x + 1, y + 1], [x, y + 1]]), 'B': [], 'Z': [],
                                'G': [], 'S': []}
            for _0 in range(0, len(MAP['B'])):
                if MAP['Q'][(x, y)]['p'].intersects(MAP['B'][_0]):
                    MAP['Q'][(x, y)]['B'].append(_0)
                    # print(_0)
                if MAP['Q'][(x, y)]['p'].intersects(MAP['Z'][_0]):
                    MAP['Q'][(x, y)]['Z'].append(_0)
                try:
                    if MAP['Q'][(x, y)]['p'].intersects(MAP['G'][_0]):
                        MAP['Q'][(x, y)]['G'].append(_0)
                except:
                    pass
    for _ in range(0, int(256 * 256)):
        try:
            #     deg = random.random() * math.pi*2
            #     dis = 100*random.random()
            X = 10 + random.random() * 236
            Y = 10 + random.random() * 236
            poly = generatePolygon(X, Y, 0.1 + random.random() * 0.1, 0.75, 0.75,
                                   random.randint(6, 8))  # 128+math.cos(deg)*dis,128+math.sin(deg)*dis
            poly = smoothPolygon(poly, 0.8)
            poly = Polygon(poly)
            if poly.area > 0.0075:
                g = False
                z = False
                b = False

                for x in range(int(X // 1 - 1), int(X // 1 + 1)):
                    for y in range(int(Y // 1 - 1), int(Y // 1 + 1)):
                        for i in MAP['Q'][(x, y)]['B']:
                            if MAP['B'][i].intersects(poly):
                                b = True
                        for i in MAP['Q'][(x, y)]['G']:
                            if MAP['G'][i].intersects(poly):
                                g = True
                        for i in MAP['Q'][(x, y)]['Z']:
                            if MAP['Z'][i].intersects(poly):
                                z = True
                        for i in MAP['Q'][(x, y)]['S']:
                            if MAP['S'][i].intersects(poly):
                                continue
                if g or z or b:
                    pass
                else:
                    if random.randint(0, 2) > 0:
                        continue
                MAP['S'].append(poly)
                for x in range(int(X // 1 - 1), int(X // 1 + 1)):
                    for y in range(int(Y // 1 - 1), int(Y // 1 + 1)):
                        if MAP['Q'][(x, y)]['p'].intersects(poly):
                            MAP['Q'][(x, y)]['S'].append(len(MAP['S']) - 1)

            # zone = LinearRing(poly).parallel_offset(1.0, 'right', join_style=2)
            # ground = LinearRing(poly).parallel_offset(-0.5, 'right', join_style=2)
            # ln = LinearRing(poly)
            # poly = Polygon(poly)
            # if g and (ground.intersects(ln) or ground.intersects(zone)): continue
            # if tuple(zone.coords) == (): continue
            # if g and tuple(ground.coords) == (): continue
            # if g and ground.area > poly.area: continue
            # zone = Polygon(zone.coords)
            # if g: ground = Polygon(ground.coords)
            # ok = True

            # for _0 in OFICIAL-MAP0['Z']:
            #     if _0.intersects(poly): ok = False
            # if ok:
            #     OFICIAL-MAP0['B'].append(poly)
            #     OFICIAL-MAP0['Z'].append(zone)
            #     if g: OFICIAL-MAP0['G'].append(ground)
        except Exception:
            logging.exception("message")
            # print(_0)
            # print(x,y)
    pickle.dump(MAP, open('MAPEXP1', 'wb'))


if __name__ == '__main__':
    main()
