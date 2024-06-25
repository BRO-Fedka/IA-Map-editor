class A():
    def __init__(self):
        print(self.__name__)


class B(A):
    pass


class C(A):
    pass


class D(B):
    pass


class E(B):
    pass


def get_finite_inherits(cls):
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


print(get_finite_inherits(A))
