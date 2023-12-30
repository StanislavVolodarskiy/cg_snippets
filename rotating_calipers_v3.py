import ast
import functools
import sys


def rot0(v):
    return v


def rot90(v):
    x, y = v
    return -y, x


def rot180(v):
    x, y = v
    return -x, -y


def rot270(v):
    x, y = v
    return y, -x


rots = rot0, rot270, rot180, rot90


def extremal_index(points, rot):
    return min(enumerate(points), key=lambda r: rot(r[1]))[0]


def find_extr(points):
    return [extremal_index(points, rot) for rot in rots]


def edge(points, index):
    return sub(points[index], points[(index + 1) % len(points)])


def get_angles(points, indices): #находим минимальный угол и получаем индекс, который необходимо изменить

    def cmp_(c1, c2):
        a = cross(c1[1], c2[1])
        if a < 0:
            return -1
        if a > 0:
            return 1
        return 0

    calipers = [
        rot(edge(points, index))
        for rot, index in zip(rots, indices)
    ]

    return min(enumerate(calipers), key=functools.cmp_to_key(cmp_))[0]


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


def rectangle_area(points, indices, index_to_change):
    indices = indices[index_to_change:] + indices[:index_to_change]

    p_bottom = points[indices[0]]
    p_right = points[indices[1]]
    p_top = points[indices[2]]
    p_left = points[indices[3]]
    h_dir = edge(points, indices[0])

    height = cross(sub(p_bottom, p_top), h_dir)
    width = dot(sub(p_left, p_right), h_dir)

    numerator = height * width
    denominator = norm2(h_dir)

    return numerator, denominator


def find_min_area(points):
    indices = find_extr(points)

    def areas():
        for _ in range(len(points)):
            index_to_change = get_angles(points, indices)
            area = rectangle_area(points, indices, index_to_change)
            yield area
            indices[index_to_change] = (indices[index_to_change] + 1) % len(points)

    def cmp_(a, b):
        na, da = a
        nb, db = b
        diff = na * db - nb * da
        if diff < 0:
            return -1
        if diff > 0:
            return 1
        return 0

    min_area = min(areas(), key=functools.cmp_to_key(cmp_))
    return min_area


def main():
    points = [ast.literal_eval(line) for line in sys.stdin]
    print(*find_min_area(points))


main()
