#!/usr/bin/env python3
# debugging.. dont know why there is a wierd point
# somehow 2-opt is not working

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

def make_convexhull(cities, indexed_cities, inner_points):
    indexed_cities.sort()
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

def greedy_insertion(convex_hull, unvisited, dist):
    for city in unvisited:
        min_dist = 1000000
        connect_edge = None
        for i in range(len(convex_hull)):
            candicate_dist = dist[city][convex_hull[i]] + dist[city][convex_hull[(i+1) % len(convex_hull)]] - dist[convex_hull[i]][convex_hull[(i+1) % len(convex_hull)]]
            if candicate_dist < min_dist:
                min_dist = candicate_dist
                connect_edge = (i+1) % len(convex_hull)
        convex_hull.insert(connect_edge, city)
    return convex_hull
    
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
                    q2 = 0
                else:
                    q2 = tour[j+1]
                if intersect(cities[p1],cities[p2],cities[q1],cities[q2]):
                    tour[i+1] = q1
                    tour[j]   = p2
                    tour[i+2:j] = reversed(tour[i+2:j])
                    updated = True
                    break
        iteration += 1
        if iteration%100 == 0:
            print('stopped opt2 iteration:', iteration)
            break
    return iteration

def solve(cities):
    # calculating dist of two nodes
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    calc_dist(dist, cities, N)
    
    prep_time = time.time()
    
    # make convex hull
    indexed_cities = [(cities[i][0], cities[i][1], i) for i in range(N)]
    inner_points = [[False, False] for i in range(N)]
    convex_hull = make_convexhull(cities, indexed_cities, inner_points)
    unvisited = []
    for i in range(N):
        if inner_points[i][0] and inner_points[i][1]:
            unvisited.append(i)
            
    # greedy insertion for inner points
    tour = greedy_insertion(convex_hull, unvisited, dist)
    
    convex_greedy_time = time.time()
    print('convex_hull based greedy done!', convex_greedy_time - prep_time)
    
    # opt-2
    iteration = opt2(tour, cities)
    
    opt2_time = time.time()
    print('opt2 done! (iteration={})'.format(iteration), opt2_time - convex_greedy_time)
    
    # sequent point re-insertion
    
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
