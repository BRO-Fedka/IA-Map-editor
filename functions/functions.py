from typing import *


def get_finite_inherits(cls: Type[object]):
    finite_inherits = []

    def f(_cls):
        subclasses = _cls.__subclasses__()
        if len(subclasses) == 0:
            finite_inherits.append(_cls)
        else:
            for sc in subclasses:
                f(sc)

    f(cls)
    return finite_inherits


def hex_to_rgb(hex: str) -> tuple:
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))


def is_сonvex(points: List) -> bool:
    def cross_product(A):
        X1 = (A[1][0] - A[0][0])

        Y1 = (A[1][1] - A[0][1])

        X2 = (A[2][0] - A[0][0])

        Y2 = (A[2][1] - A[0][1])

        return (X1 * Y2 - Y1 * X2)

    N = len(points)
    prev = 0
    curr = 0
    for i in range(N):
        temp = [points[i], points[(i + 1) % N],
                points[(i + 2) % N]]
        curr = cross_product(temp)
        if (curr != 0):
            if (curr * prev < 0):
                return False
            else:
                prev = curr

    return True
