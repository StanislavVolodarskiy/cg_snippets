import ast
import functools


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


def triangle_area(point1, point2):
    return point2[0] * point1[1] - point1[0] * point2[1]


def edge(points, index):
    x1, y1 = points[index]
    x2, y2 = points[(index + 1) % len(points)]
    return x2 - x1, y2 - y1


def get_angles(points, indices): #находим минимальный угол и получаем индекс, который необходимо изменить

    calipers = [
        rot(edge(points, index))
        for rot, index in zip(rots, indices)
    ]

    new_points = [(calipers[i][0], calipers[i][1], i) for i in range(4)]

    def cmp_(c1, c2):
        a = triangle_area(c1[:2], c2[:2])
        if a < 0:
            return -1
        if a > 0:
            return 1
        return 0

    return min(new_points, key=functools.cmp_to_key(cmp_))[2]


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


def norm(v):
    x, y = v
    return (x * x + y * y) ** 0.5


def rectangle_area(points, indices, index_to_change):
    indices = indices[index_to_change:] + indices[:index_to_change]

    p_bottom = points[indices[0]]
    p_right = points[indices[1]]
    p_top = points[indices[2]]
    p_left = points[indices[3]]
    h_dir = sub(p_bottom, points[(indices[0] + 1) % len(points)])

    height = cross(sub(p_bottom, p_top), h_dir) / norm(h_dir)

    width = dot(sub(p_left, p_right), h_dir) / norm(h_dir)

    rect_area = width * height

    return rect_area


def find_min_area(points):
    indices = find_extr(points)

    def areas():
        for _ in range(len(points)):
            index_to_change = get_angles(points, indices)
            area = rectangle_area(points, indices, index_to_change)
            yield area
            indices[index_to_change] = (indices[index_to_change] + 1) % len(points)

    min_area = min(areas())
    return min_area


def main():
    with open('polygon_points.txt', 'r') as f:
        lines = f.read().split('\n')
    points = [ast.literal_eval(line) for line in lines]

    min_rectangle_area = find_min_area(points)
    print(min_rectangle_area)


main()
