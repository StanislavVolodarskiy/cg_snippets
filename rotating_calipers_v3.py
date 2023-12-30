import ast
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


def get_angles(points, points_indexes): #находим минимальный угол и получаем индекс, который необходимо изменить

    calipers = [
        rot(edge(points, index))
        for rot, index in zip(rots, points_indexes)
    ]
    
    new_points = [(calipers[i][0], calipers[i][1], i) for i in range(4)]

    def less(c1, c2):
        return triangle_area(c1[:2], c2[:2]) < 0
    
    min_caliper = new_points[0]
    for j in range(1,4):
        if less(new_points[j], min_caliper):
            min_caliper = new_points[j]
    
    return min_caliper[2]
    

def change_indexes(points, points_indexes, index_to_change): #пересчет индексов
    new_points_indexes = points_indexes.copy()
    new_points_indexes[index_to_change] = (new_points_indexes[index_to_change] + 1) % len(points)
    return new_points_indexes


def rectangle_area(points, points_indexes, index_to_change):
    points_indexes = points_indexes[index_to_change:] + points_indexes[:index_to_change]

    norm = np.linalg.norm

    p_bottom = np.array(points[points_indexes[0]])
    p_right = np.array(points[points_indexes[1]])
    p_top = np.array(points[points_indexes[2]])
    p_left = np.array(points[points_indexes[3]])
    h_dir = np.array(points[(points_indexes[0] + 1) % len(points)]) - p_bottom

    height = norm(np.cross(p_top - p_bottom, h_dir)) / norm(h_dir)

    width = np.dot(p_right - p_left, h_dir) / norm(h_dir)

    rect_area = width * height

    return rect_area
    

def find_min_area(points):

    start_points_indexes = find_extr(points)
    all_areas = []
    index_to_change = get_angles(points, start_points_indexes)
    all_areas.append(rectangle_area(points, start_points_indexes, index_to_change))
    points_indexes = change_indexes(points, start_points_indexes, index_to_change)  
    
    for i in range(len(points)-1):
        index_to_change = get_angles(points, points_indexes)
        area = rectangle_area(points, points_indexes, index_to_change)
        all_areas.append(area)
        points_indexes = change_indexes(points, points_indexes, index_to_change)
            
        i+=1
    min_area = min(all_areas)
    return min_area


def main():
    with open('polygon_points.txt', 'r') as f:
        lines = f.read().split('\n')
    points = [ast.literal_eval(line) for line in lines]

    min_rectangle_area = find_min_area(points)
    print(min_rectangle_area)


main()
