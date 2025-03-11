from shapely.geometry import *
from shapely.ops import *
import matplotlib.pyplot as plt
from random import *
from typing import *
import numpy
import math
import networkx as nx


def segments(curve):
    return list(map(LineString, zip(curve.coords[:-1], curve.coords[1:])))


def polysegs(poly):
    return segments(LinearRing(list(poly.exterior.coords[:])))


def clip(x, min, max):
    if (min > max):
        return x
    elif (x < min):
        return min
    elif (x > max):
        return max
    else:
        return x


def lookat(x, y):
    if x == 0:
        x = 0.001
    angle = math.atan((y / x)) / (math.pi / 180)
    if y != abs(y):
        angle = angle + 360
    if x != abs(x):
        angle = angle + 180
    return angle % 360


def generatePolygon2(p):
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
        tmp = uniform(lower, upper)
        angleSteps.append(tmp)
        sum = sum + tmp
    k = sum / (2 * math.pi)
    for i in range(numVerts):
        angleSteps[i] = angleSteps[i] / k
    points = []
    angle = uniform(0, 2 * math.pi)
    for i in range(numVerts):
        r_i = clip(gauss(aveRadius, spikeyness), 0, 2 * aveRadius)
        x = ctrX + r_i * math.cos(angle)
        y = ctrY + r_i * math.sin(angle)
        points.append((x, y))
        angle = angle + angleSteps[i]
    return points


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

################
# Как создаётся остров:
################

# p = generatePolygon2(generatePolygon(center_x, center_y, r, 0.5, 0.5,vertices))

# for _ in range(0, 2):
#     p = smoothPolygon(p, 2)
# for _ in range(0, 2):
#     p = smoothPolygon(p, 1)
# p - остров в формате [(x,y),(x,y)]
