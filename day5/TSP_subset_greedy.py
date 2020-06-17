#!/usr/bin/env python3

import sys
import math
import time
from collections import deque

from common import print_tour, read_input, format_tour

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def area(p,q,r):
    return ((q[0]-p[0])*(r[1]-p[1])-(r[0]-p[0])*(q[1]-p[1]))/2.0

def intersect(p1,p2,q1,q2):
    #if p1=q1 or something like that, return False because area() should be zero
    return (area(p1,p2,q1)*area(p1,p2,q2)<0) and (area(q1,q2,p1)*area(q1,q2,p2)<0)

def isopt(new_city, candicate_index, tour_index, cities):
    p1 = tour_index[candicate_index]
    p2 = new_city
    p3 = tour_index[candicate_index+1]   
    for i in range(len(tour_index)-1):
        if intersect(cities[p1], cities[p2], cities[tour_index[i]], cities[tour_index[i+1]]):
                return False
        if intersect(cities[p2], cities[p3], cities[tour_index[i]], cities[tour_index[i+1]]):
                return False
    return True

def solve(cities):
    N = len(cities)
    sorted_ = list(sorted([[cities[i][0], cities[i][1], i] for i in range(N)]))
    indexes = []
    del cities[:]
    for i in range(N):
        indexes.append(sorted_[i][2])
        cities.append([sorted_[i][0], sorted_[i][1]])
    #preparetion
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    #TSP -> expecting total time = O(N^2)
    unvisited_cities = deque([i for i in range(len(cities))])
    tour_index = []
    #create triangle
    for i in range(3):
        tour_index.append(unvisited_cities.popleft())
    tour_index.append(tour_index[0])
    #add cities one by one and make convex
    while len(unvisited_cities):
        new_city = unvisited_cities.popleft()
        reconnect_index = None
        for candicate_index in range(1, len(tour_index)):
            if isopt(new_city, candicate_index, tour_index, cities):
                reconnect_index = candicate_index
                break
        tour_index.insert(reconnect_index+1, new_city)
    tour = []
    for index in tour_index:
        tour.append(indexes[index])
    return tour[:-1]

if __name__ == '__main__':
    assert len(sys.argv) > 1
    start = time.time()
    tour = solve(read_input('input_{}.csv'.format(sys.argv[1])))
    with open(f'output_{sys.argv[1]}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')
    #print_tour(tour)
    end = time.time()
    print('whole time', end-start)
