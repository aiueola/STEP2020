#!/usr/bin/env python3

import sys
import math
import time
import copy

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
        
def length_of_tour(tour, N, dist):
    return sum(dist[tour[i]][tour[(i + 1) % N]] for i in range(N))
        
def update_tour(last_node, tour, min_dist, N, prev_nodes, dist):
    temp_tour = [last_node]
    prev_node = prev_nodes[last_node][-1]
    while prev_node:
        temp_tour.append(prev_node)
        try:
            prev_node = prev_nodes[prev_node][-1]
        except:
            prev_node = None
    temp_tour.append(0)
    temp_len = length_of_tour(temp_tour, N, dist)
    if temp_len < min_dist[0]:
        tour[0] = temp_tour
        min_dist[0] = temp_len
        
def search_path(neighbors, visited, prev_nodes, num_of_visited, current_node, prev_node, N, tour, min_dist, dist):
    if visited[current_node] == True:
        return
    
    if prev_node:
        prev_nodes[current_node].append(prev_node)
    visited[current_node] = True
    num_of_visited += 1   
    
    if num_of_visited == N:
        update_tour(current_node, tour, min_dist, N, prev_nodes, dist)
        visited[current_node] = False
        prev_nodes[current_node].pop()
        return
    
    for next_node in neighbors[current_node]:
        search_path(neighbors, visited, prev_nodes, num_of_visited, next_node, current_node, N, tour, min_dist, dist)
    visited[current_node] = False
    if prev_node:
        prev_nodes[current_node].pop()
    return

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
    find_neighbors(neighbors, dist, N, 5)
            
    # find ways using depth first search + prune edges
    # though this algorithm prune edges, this seems too slow.
    visited = [False for i in range(N)]
    prev_nodes = [[] for i in range(N)]
    num_of_visited = 0
    current_node = 0
    prev_node = None
    tour = [False]
    min_dist = [1000000]
    search_path(neighbors, visited, prev_nodes, num_of_visited, current_node, prev_node, N, tour, min_dist, dist)
    return tour[0] 

if __name__ == '__main__':
    assert len(sys.argv) > 1
    start = time.time()
    tour = solve(read_input('input_{}.csv'.format(sys.argv[1])))
    with open(f'output_{sys.argv[1]}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')
    #print_tour(tour)
    end = time.time()
    print('whole time', end-start)
