import functools
import sys


def sub(p1, p2):
    """ p2 - p1 """

    x1, y1 = p1
    x2, y2 = p2
    return x2 - x1, y2 - y1


def dot(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return x1 * x2 + y1 * y2


def cross(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return y1 * x2 - x1 * y2


def norm2(v):
    x, y = v
    return x * x + y * y


rots =                        \
    lambda v:   v           , \
    lambda v: ( v[1], -v[0]), \
    lambda v: (-v[0], -v[1]), \
    lambda v: (-v[1],  v[0])


def extremal_index(points, rot):
    return min(enumerate(points), key=lambda r: rot(r[1]))[0]


def edge(points, index):
    return sub(points[index], points[(index + 1) % len(points)])


def get_angles(points, indices):

    def cmp_(c1, c2):
        return cross(c1[1], c2[1])

    calipers = [
        rot(edge(points, index))
        for rot, index in zip(rots, indices)
    ]

    i = min(enumerate(calipers), key=functools.cmp_to_key(cmp_))[0]
    return indices[i:] + indices[:i]


def rectangle_area(points, indices):
    h_dir = edge(points, indices[0])
    height = cross(sub(points[indices[0]], points[indices[2]]), h_dir)
    width  = dot  (sub(points[indices[3]], points[indices[1]]), h_dir)
    return height * width, norm2(h_dir)


def find_min_area(points):

    def areas(indices):
        for _ in range(len(points)):
            indices = get_angles(points, indices)
            yield rectangle_area(points, indices)
            indices[0] = (indices[0] + 1) % len(points)

    def cmp_(a, b):
        na, da = a
        nb, db = b
        return na * db - nb * da

    return min(
        areas([extremal_index(points, rot) for rot in rots]),
        key=functools.cmp_to_key(cmp_)
    )


print(*find_min_area([tuple(map(int, line.split())) for line in sys.stdin]))
