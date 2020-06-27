#!/usr/bin/env python3

import sys
import math
import time

from common import print_tour, read_input, format_tour


def read_input_parallel(filename):
    with open(filename) as f:
        area_cities = []
        for line in f.readlines()[1:]:  # Ignore the first line.
            x_y_index = line.split(',')
            area_cities.append((float(x_y_index[0]), float(x_y_index[1]), int(x_y_index[2])))
        return area_cities

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def area(p,q,r):
    return ((q[0]-p[0])*(r[1]-p[1])-(r[0]-p[0])*(q[1]-p[1]))/2.0

def intersect(p1,p2,q1,q2):
    return (area(p1,p2,q1)*area(p1,p2,q2)<0) and (area(q1,q2,p1)*area(q1,q2,p2)<0)

def solve(area_cities):
    N = len(area_cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(area_cities[i], area_cities[j])
            
    #greedy_first
    current_city = 0
    unvisited_cities = set(range(1, N))
    area_tour = [current_city]
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        area_tour.append(next_city)
        current_city = next_city
    greedy = time.time()
    print('greedy done!', greedy-start)
    
    #opt-2
    iteration = 0
    updated = True
    while updated:
        updated = False
        for i in range(len(area_tour)-2):
            p1 = area_tour[i]
            p2 = area_tour[i+1]
            for j in range(i+2, len(area_tour)):
                q1 = area_tour[j]
                if j == len(area_tour)-1:
                    q2 = 0
                else:
                    q2 = area_tour[j+1]
                if intersect(area_cities[p1], area_cities[p2], area_cities[q1], area_cities[q2]):
                    area_tour[i+1] = q1
                    area_tour[j]   = p2
                    area_tour[i+2:j] = reversed(area_tour[i+2:j])
                    updated = True
                    break
        iteration += 1
        if iteration%100 == 0:
            print('iteration:', iteration)
    
    opt2 = time.time()
    print('opt2 done! (iteration={})'.format(iteration), opt2-greedy)
    
    tour = []
    for i in range(len(area_tour)):
        tour.append(area_cities[area_tour[i]][2])
    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    start = time.time()
    tour = solve(read_input_parallel('input_{}.csv'.format(sys.argv[1])))        
    with open(f'output_{sys.argv[1]}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')
    #print_tour(tour)
    end = time.time()
    print('whole time', end-start)
