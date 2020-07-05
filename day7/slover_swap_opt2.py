#!/usr/bin/env python3
# debugging.. somehow swap_opt iteration doesnt finish

import sys
import math
import time
import copy

from common import print_tour, read_input, format_tour


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def swap_nodes(tour, swap_node1, swap_node2):
    temp1 = tour[swap_node1]
    temp2 = tour[swap_node2]
    tour[swap_node1] = temp2
    tour[swap_node2] = temp1
    
def total_dist(tour, dist):
    return sum(dist[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))

def swap_opt(tour, cities, dist):
    # dont know why this iteration goes to infinity
    N = len(tour)
    iteration = 0
    updated = True
    while updated:
        updated = False
        for i in range(N-1):
            for j in range(i+3, N):
                if (i - j) % N > 2:
                    change_in_dist = dist[(i-1)%N][j] + dist[j][i+1] + dist[j-1][i] + dist[i][(j+1)%N] - (dist[(i-1)%N][i] + dist[i][i+1] + dist[j-1][j] + dist[j][(j+1)%N])
                if change_in_dist < 0:
                    swap_nodes(tour, i, j)
                    updated = True
                    break
        iteration += 1
        if iteration%100 == 0:
            print('iteration:', iteration)
    return iteration

def area(p,q,r):
    return ((q[0]-p[0])*(r[1]-p[1])-(r[0]-p[0])*(q[1]-p[1]))/2.0

def intersect(p1,p2,q1,q2):
    return (area(p1,p2,q1)*area(p1,p2,q2)<0) and (area(q1,q2,p1)*area(q1,q2,p2)<0)

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
            print('iteration:', iteration)
    return iteration
        

def solve(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
            
    prep_time = time.time()
            
    # greedy_first
    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    greedy_time = time.time()
    print('greedy done!', greedy_time - prep_time)
    
    # swap_opt
    iteration = swap_opt(tour, cities, dist)
    swap_time = time.time()
    print('swap_opt done! (iteration={})'.format(iteration), swap_time - greedy_time)
     
    # 2-opt
    iteration = opt2(tour, cities)
    opt2_time = time.time()
    print('opt2 done! (iteration={})'.format(iteration), opt2_time - swap_time)
    
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
