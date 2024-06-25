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
