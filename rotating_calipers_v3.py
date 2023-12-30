import ast
import functools
import numpy as np


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
    extremum = min(
        ((p, i) for i, p in enumerate(points)),
        key=lambda r: rot(r[0])
    )
    return extremum[-1]


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

    def less(c1, c2):
        return triangle_area(c1[:2], c2[:2]) < 0

    return max(new_points, key=functools.cmp_to_key(less))[2]


def rectangle_area(points, indices, index_to_change):
    indices = indices[index_to_change:] + indices[:index_to_change]

    norm = np.linalg.norm

    p_bottom = np.array(points[indices[0]])
    p_right = np.array(points[indices[1]])
    p_top = np.array(points[indices[2]])
    p_left = np.array(points[indices[3]])
    h_dir = np.array(points[(indices[0] + 1) % len(points)]) - p_bottom

    height = norm(np.cross(p_top - p_bottom, h_dir)) / norm(h_dir)

    width = np.dot(p_right - p_left, h_dir) / norm(h_dir)

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
