#!/usr/bin/env python3

import sys
import math
import time
import copy
import random
import numpy as np

from common import print_tour, read_input, format_tour


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def calc_prob(change_in_dist, iteration):
    if change_in_dist > 0:
        return min(0.001 + 0.9 / (iteration + 1), 0.3)
    else:
        return max(0.9 - 0.9 / (iteration + 1), 0.7)
    
def swap_nodes(swap_node1, swap_node2, tour):
    temp1 = tour[swap_node1]
    temp2 = tour[swap_node2]
    tour[swap_node1] = temp2
    tour[swap_node2] = temp1
    
def total_dist(tour, dist, N):
    return sum(dist[tour[i]][tour[(i + 1) % N]] for i in range(N))

def area(p,q,r):
    return ((q[0]-p[0])*(r[1]-p[1])-(r[0]-p[0])*(q[1]-p[1]))/2.0

def intersect(p1,p2,q1,q2):
    return (area(p1,p2,q1)*area(p1,p2,q2)<0) and (area(q1,q2,p1)*area(q1,q2,p2)<0)

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
    print('iteration={}, total_dist={}'.format(0, total_dist(tour, dist, N)))
    
    # SA
    iteration = 0
    while iteration < 1000:
        # swap_opt
        swap_node1 = random.randrange(N)
        swap_node2 = (swap_node1+1) % N
        #swap_node2 = random.randrange(N)
        #if swap_node1 == swap_node2:
        #    pass
        new_tour = copy.copy(tour)
        swap_nodes(swap_node1, swap_node2, new_tour)
        change_in_dist = total_dist(new_tour, dist, N) - total_dist(tour, dist, N)
        prob = calc_prob(change_in_dist, iteration)
        if random.random() < prob:
            del tour[:]
            tour = new_tour
        else:
            del new_tour[:]
            
        # 2-opt
        for i in range(len(tour)-2):
            p1 = tour[i]
            p2 = tour[i+1]
            for j in range(i+2, len(tour)):
                q1 = tour[j]
                if j == len(tour)-1:
                    q2 = tour[0]
                else:
                    q2 = tour[j+1]
                if intersect(cities[p1],cities[p2],cities[q1],cities[q2]) and random.random() < calc_prob(-1, iteration):
                    tour[i+1] = q1
                    tour[j]   = p2
                    tour[i+2:j] = reversed(tour[i+2:j])
                    break
                    
        iteration += 1
        if iteration < 21:
            print('iteration={}, total_dist={}'.format(iteration, total_dist(tour, dist, N)))
        if (iteration % 100 == 0):
            print('iteration={}, total_dist={}'.format(iteration, total_dist(tour, dist, N)))
        
    sa_time = time.time()
    print('SA done! (iteration={})'.format(iteration), sa_time - greedy_time)
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
