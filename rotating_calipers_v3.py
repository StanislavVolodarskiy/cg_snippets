import numpy as np
# import pandas as pd
import math
import ast

with open('polygon_points.txt', 'r') as f:
    lines = f.read().split('\n')
points = [ast.literal_eval(line) for line in lines]
points

def find_extr(points):
    bottom_min = min([ point[1] for point in points])
    points_filter = [point for point in points if point[1]==bottom_min]
    bottom_p = sorted(points_filter, key = lambda x: x[0], reverse=True)[0]
    
    right_max = max([point[0] for point in points])
    points_filter = [point for point in points if point[0]==right_max]
    right_p = sorted(points_filter, key = lambda x: x[1], reverse = True)[0]
    
    top_max = max([point[1] for point in points])
    points_filter = [point for point in points if point[1]==top_max]
    top_p = sorted(points_filter, key = lambda x: x[0])[0]
    
    left_min = min([ point[0] for point in points])
    points_filter = [point for point in points if point[0]==left_min]
    left_p = sorted(points_filter, key = lambda x: x[1])[0]

    
    return bottom_p, right_p, top_p, left_p

bottom_p, right_p, top_p, left_p = find_extr(points)
bottom_p, right_p, top_p, left_p #4 экстремальные точки

start_points_indexes = [points.index(bottom_p), points.index(right_p), points.index(top_p), points.index(left_p)]
start_points_indexes #стартовый набор точек калиперов

def triangle_area(point1, point2):
    
    S = 1/2 * (point2[0]*point1[1] - point1[0]*point2[1])
    
    return S

def rotate_caliper(point1, point2, angle):

    new_x = point1[0] + (point2[0] - point1[0])*math.cos(angle) - (point2[1] - point1[1])*math.sin(angle)
    new_y = point1[1] + (point2[0] - point1[0])*math.sin(angle) + (point2[1] - point1[1])*math.cos(angle)

    return (new_x, new_y)

def get_angles(points_indexes): #находим минимальный угол и получаем индекс, который необходимо изменить
    
    bottom_caliper = points[(points_indexes[0]+1) % len(points)]
    right_caliper = rotate_caliper(points[points_indexes[1]], points[(points_indexes[1]+1) % len(points)], 3/2*math.pi)
    top_caliper = rotate_caliper(points[points_indexes[2]], points[(points_indexes[2]+1) % len(points)], math.pi)
    left_caliper = rotate_caliper(points[points_indexes[3]], points[(points_indexes[3]+1) % len(points)], math.pi/2)

    calipers = [bottom_caliper, right_caliper, top_caliper, left_caliper]
    
    new_points = [(calipers[i][0] - points[points_indexes[i]][0], calipers[i][1] - points[points_indexes[i]][1], 
                   points_indexes[i]) for i in range(4)]

    areas = []
    for i in range(4):
        for j in range(1,4):
            p1 = (new_points[i][0], new_points[i][1])
            p2 = (new_points[j][0], new_points[j][1])
            areas.append((triangle_area(p1, p2), new_points[i], new_points[j]))
    areas.sort(key = lambda x: x[0])
    
    min_ang = areas[0]
    
    ind_to_change = min_ang[1][2]
    
    return ind_to_change
    

# get_angles(start_points_indexes)

def change_indexes(points_indexes, index_to_change): #пересчет индексов
    new_points_indexes = points_indexes.copy()
    new_points_indexes[new_points_indexes.index(index_to_change)] = (index_to_change + 1) % len(points)
    return new_points_indexes


def rectangle_area(points_indexes):
    norm = np.linalg.norm

    p1 = np.array(points[(points_indexes[0] - 1) % len(points)])
    p2 = np.array(points[points_indexes[0]])
    p3 = np.array(points[points_indexes[2]])

    d1 = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)

    p1 = np.array(points[(points_indexes[1] - 1) % len(points)])
    p2 = np.array(points[points_indexes[1]])
    p3 = np.array(points[points_indexes[3]])

    d2 = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)

    rect_area = d1 * d1

    return rect_area
    

def find_min_area(points):

    bottom_p, right_p, top_p, left_p = find_extr(points)
    start_points_indexes = [points.index(bottom_p), points.index(right_p), points.index(top_p), points.index(left_p)]
    all_areas = []
    all_areas.append(rectangle_area(start_points_indexes))
    index_to_change = get_angles(start_points_indexes)
    points_indexes = change_indexes(start_points_indexes, index_to_change)  
    
    for i in range(len(points)-1):
        if points_indexes != start_points_indexes and len(points_indexes) == len(set(points_indexes)):
            area = rectangle_area(points_indexes)
            all_areas.append(area)
            index_to_change = get_angles(points_indexes)
            points_indexes = change_indexes(points_indexes, index_to_change)
            
        i+=1
    min_area = min(all_areas)
    return min_area

min_rectangle_area = find_min_area(points)

print(min_rectangle_area)
