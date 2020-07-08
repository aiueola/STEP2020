#!/usr/bin/env python3
# also, this seems not efficient

import sys
import math
import time

from common import print_tour, read_input, format_tour


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def calc_dist(dist, cities, N):
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

def area(p,q,r):
    return ((q[0]-p[0])*(r[1]-p[1])-(r[0]-p[0])*(q[1]-p[1]))/2.0

def intersect(p1,p2,q1,q2):
    return (area(p1,p2,q1)*area(p1,p2,q2)<0) and (area(q1,q2,p1)*area(q1,q2,p2)<0)

def find_indexed_city(indexed_cities, i):
    for j in range(len(indexed_cities)):
        if indexed_cities[j][2] == i:
            return [indexed_cities[j][0], indexed_cities[j][1], indexed_cities[j][2]]

def make_convex_hull(cities, indexed_cities, inner_points):
    lower = []
    for indexed_city in indexed_cities:
        while len(lower)>=2 and area(cities[lower[-2]], cities[lower[-1]] , cities[indexed_city[2]])<=0:
            inner_points[lower.pop()][0] = True
        lower.append(indexed_city[2])
    upper = []
    for indexed_city in reversed(indexed_cities):
        while len(upper)>=2 and area(cities[upper[-2]], cities[upper[-1]], cities[indexed_city[2]])<=0:
            inner_points[upper.pop()][1] = True
        upper.append(indexed_city[2])
    return lower[1:] + upper[1:]

def greedy_insertion(outer, next_layer, dist):
    for city in next_layer:
        min_dist = 1000000
        connect_edge = None
        for i in range(len(outer)):
            candicate_dist = dist[city][outer[i]] + dist[city][outer[(i+1) % len(outer)]] - dist[outer[i]][outer[(i+1) % len(outer)]]
            if candicate_dist < min_dist:
                min_dist = candicate_dist
                connect_edge = (i+1) % len(outer)
        outer.insert(connect_edge, city)
    return outer

def opt2(tour, cities):
    iteration = 0
    updated = True
    while updated:
        updated = False
        for i in range(len(tour)-2):
            p1 = tour[i]
            p2 = tour[i+1]
            for j in range(i+2, len(tour)):
                q1 = tour[j]
                if j == len(tour)-1:
                    q2 = tour[0]
                else:
                    q2 = tour[j+1]
                if intersect(cities[p1],cities[p2],cities[q1],cities[q2]):
                    tour[i+1] = q1
                    tour[j]   = p2
                    tour[i+2:j] = reversed(tour[i+2:j])
                    updated = True
                    break
        iteration += 1
    return iteration, tour

def solve(cities):
    # calculating dist of two nodes
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    calc_dist(dist, cities, N)
    
    prep_time = time.time()
        
    # make tour from outer part to inner part
    # make first convex hull
    indexed_cities = sorted([(cities[i], cities[i], i) for i in range(N)])
    inner_points = [[False, False] for i in range(N)]
    outer = make_convex_hull(cities, indexed_cities, inner_points)
    new_indexed_cities = []
    for i in range(N):
        if inner_points[i][0] and inner_points[i][1]:
            new_indexed_cities.append(find_indexed_city(indexed_cities, i))
    del indexed_cities[:], inner_points[:]
    indexed_cities = sorted(new_indexed_cities)
    
    iteration = 0
    while indexed_cities:
        # make convex hull for unvisited cities
        if len(indexed_cities) > 3:
            inner_points = [[False, False] for i in range(N)]
            next_layer = make_convex_hull(cities, indexed_cities, inner_points)
            new_indexed_cities = []
            for i in range(N):
                if inner_points[i][0] and inner_points[i][1]:
                    new_indexed_cities.append(find_indexed_city(indexed_cities, i))
            del indexed_cities[:], inner_points[:]
            indexed_cities = sorted(new_indexed_cities)       
        else:
            next_layer = [indexed_cities[i][2] for i in range(len(indexed_cities))]
            del indexed_cities[:]
        
        # greedy insertion for next convex hull points
        outer = greedy_insertion(outer, next_layer, dist)
        iteration += 1
    
    convex_hull_time = time.time()
    print('convex hull insertion done! (iteration={})'.format(iteration), convex_hull_time - prep_time)
    
    # 2-opt
    iteration, tour = opt2(outer, cities)
    
    opt2_time = time.time()
    print('2-opt done! (iteration={})'.format(iteration), opt2_time - convex_hull_time)
    
    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    start = time.time()
    tour = solve(read_input('input_{}.csv'.format(sys.argv[1])))
    with open(f'output_{sys.argv[1]}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')
    #print_tour(tour)
    end = time.time()
    print('whole time', end-start)
