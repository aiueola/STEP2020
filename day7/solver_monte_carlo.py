#!/usr/bin/env python3

import sys
import math
import time
import copy
import random

from common import print_tour, read_input, format_tour


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def calc_dist(dist, cities, N):
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
            
def find_neighbors(neighbors, dist, N, num_of_neighbors):
    for i in range(N):
        dist_from_i = sorted([[dist[i][j], j] for j in range(N)])
        for k in range(num_of_neighbors):
            neighbors[i].append(dist_from_i[k+1][1])
        del dist_from_i[:]
        
def total_dist(tour, dist, N):
    return sum(dist[tour[i]][tour[(i + 1) % N]] for i in range(N))
        
def rollout(determined_tour, candicate, candicate_next, visited, dist):
    if visited[candicate] or visited[candicate_next]:
        return False, 0
    rollout_tour = copy.copy(determined_tour)
    rollout_visited = copy.copy(visited)
    rollout_tour.extend([candicate, candicate_next])
    rollout_visited[candicate] = True
    rollout_visited[candicate_next] = True
    unvisited = []
    for i in range(len(rollout_visited)):
        if not rollout_visited[i]:
            unvisited.append(i)
    current_city = candicate_next
    while unvisited:
        next_city = min(unvisited, key=lambda city: dist[current_city][city])
        unvisited.remove(next_city)
        rollout_tour.append(next_city)
        current_city = next_city
    rollout_dist = total_dist(rollout_tour, dist, len(rollout_tour))
    del rollout_tour[:], rollout_visited[:], unvisited[:]
    return True, rollout_dist

def find_greedy_next(determined_tour, visited, dist):
    unvisited = []
    for i in range(len(visited)):
        if not visited[i]:
            unvisited.append(i)
    current_city = determined_tour[-1]
    next_city = min(unvisited, key=lambda city: dist[current_city][city])
    del unvisited[:]
    return next_city

def area(p,q,r):
    return ((q[0]-p[0])*(r[1]-p[1])-(r[0]-p[0])*(q[1]-p[1]))/2.0

def intersect(p1,p2,q1,q2):
    return (area(p1,p2,q1)*area(p1,p2,q2)<0) and (area(q1,q2,p1)*area(q1,q2,p2)<0)

def solve(cities):
    # calculating dist of two nodes
    N = len(cities)
    dist = [[0] * N for i in range(N)]
    calc_dist(dist, cities, N)
    
    # finding neighboring nodes
    neighbors = [[] for i in range(N)]
    find_neighbors(neighbors, dist, N, 4)
    
    prep_time = time.time()
            
    # find with monte carlo tree search
    tour = []
    visited = [False for i in range(N)]
    while len(tour) < N-5:
        next_node = None
        next_ave_dist = 1000000
        if not tour:
            candicates = [random.randrange(N) for i in range(5)]
        else:
            candicates = neighbors[tour[-1]]
        for candicate in candicates:
            total_route = 0
            sum_of_dist = 0
            candicate_neighbors = neighbors[candicate]
            for candicate_neighbor in candicate_neighbors:
                is_route_exist, rollout_dist = rollout(tour, candicate, candicate_neighbor, visited, dist)
                total_route += is_route_exist
                sum_of_dist += rollout_dist
            if not total_route:
                continue
            candicate_ave_dist = sum_of_dist / total_route
            if candicate_ave_dist < next_ave_dist:
                next_node = candicate
                next_ave_dist = candicate_ave_dist
        if not next_node:
            next_node = find_greedy_next(tour, visited, dist)
        tour.append(next_node)
        visited[next_node] = True
        
    # find greedy path for remaining point
    current_city = tour[-1]
    unvisited = []
    for i in range(len(visited)):
        if not visited[i]:
            unvisited.append(i)
    while unvisited:
        next_city = min(unvisited, key=lambda city: dist[current_city][city])
        tour.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city
        
    monte_carlo_time = time.time()
    print('monte carlo based greedy done!', monte_carlo_time - prep_time)
        
    # 2-opt
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
        if iteration%100 == 0:
            print('iteration:', iteration)
    
    opt2_time = time.time()
    print('2-opt done! (iteration={})'.format(iteration), opt2_time - monte_carlo_time)
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
