#!/usr/bin/env python3

import sys
import math
import time
from threading import Thread

from common import print_tour, read_input, format_tour

    
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def area(p,q,r):
    return ((q[0]-p[0])*(r[1]-p[1])-(r[0]-p[0])*(q[1]-p[1]))/2.0

def intersect(p1,p2,q1,q2):
    return (area(p1,p2,q1)*area(p1,p2,q2)<0) and (area(q1,q2,p1)*area(q1,q2,p2)<0)

def solve_greedy(area_cities, area_tour, dist, current_city):
    unvisited_cities = set(range(1, len(area_cities)))
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        area_tour.append(next_city)
        current_city = next_city

def solve_opt2(area_cities, area_tour):
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
                    q2 = tour[0]
                else:
                    q2 = area_tour[j+1]
                if intersect(area_cities[p1], area_cities[p2], area_cities[q1], area_cities[q2]):
                    area_tour[i+1] = q1
                    area_tour[j]   = p2
                    area_tour[i+2:j] = reversed(area_tour[i+2:j])
                    updated = True
                    break

def solve_area(area_cities, result):
    N = len(area_cities)
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(area_cities[i], area_cities[j])
    #greedy_first
    current_city = 0
    area_tour = [current_city]
    solve_greedy(area_cities, area_tour, dist, current_city)
    #opt-2
    solve_opt2(area_cities, area_tour)
    
    tour = []
    for i in range(len(area_tour)):
        tour.append(area_cities[area_tour[i]][2])
    result.extend(tour)

                    
# find closest node to center in each area in order to find where to connect tour
def find_closest_to_center(area, cities):
    min_dist = 800.0**2 + 450.0**2
    closest = None
    for i in range(len(area)):
        if (cities[area[i]][0] - 800)**2 + (cities[area[i]][1] - 450)**2 < min_dist:
            min_dist = (cities[area[i]][0] - 800)**2 + (cities[area[i]][1] - 450)**2
            closest = i
    return closest
    
# this module concat four csv_file
def concat_data(upper_left, upper_right, bottom_left, bottom_right, cities):
    # find closest tour index
    upper_left_center = find_closest_to_center(upper_left, cities)
    upper_right_center = find_closest_to_center(upper_right, cities)
    bottom_left_center = find_closest_to_center(bottom_left, cities)
    bottom_right_center = find_closest_to_center(bottom_right, cities)    
    # concatenation
    tour = []
    tour.extend(upper_left[:upper_left_center])
    tour.extend(bottom_left[bottom_left_center:])
    tour.extend(bottom_left[:bottom_left_center])
    tour.extend(bottom_right[bottom_right_center:])
    tour.extend(bottom_right[:bottom_right_center])
    tour.extend(upper_right[upper_right_center:])
    tour.extend(upper_right[:upper_right_center])
    tour.extend(upper_left[upper_left_center:])
    return tour


def parallel_processing(file_num):
    # first, split data into four areas
    upper_left = []
    upper_right = []
    bottom_left = []
    bottom_right = []
    cities = read_input('input_{}.csv'.format(file_num))
    for i in range(len(cities)):
        if cities[i][0] < 800.0:
            if cities[i][1] < 450.0:
                upper_left.append((cities[i][0], cities[i][1], i))
            else:
                upper_right.append((cities[i][0], cities[i][1], i))
        else:
            if cities[i][1] < 450.0:
                bottom_left.append((cities[i][0], cities[i][1], i))
            else:
                bottom_right.append((cities[i][0], cities[i][1], i))
                
    # solve each area using threading
    upper_left_result = []
    upper_right_result = []
    bottom_left_result = []
    bottom_right_result = []
    thread1 = Thread(target=solve_area, args=(upper_left, upper_left_result))
    thread2 = Thread(target=solve_area, args=(upper_right, upper_right_result))
    thread3 = Thread(target=solve_area, args=(bottom_left, bottom_left_result))
    thread4 = Thread(target=solve_area, args=(bottom_right, bottom_right_result))
    threads = [thread1, thread2, thread3, thread4]
    for thread in threads:
        thread.start()
    # somehow this sleep makes runtime a bit faster, maybe need to wait till threads start?
    time.sleep(3)
    for thread in threads:
        thread.join()
    
    # concatenate results
    return concat_data(upper_left_result, upper_right_result, bottom_left_result, bottom_right_result, cities)


if __name__ == '__main__':
    assert len(sys.argv) > 1
    start = time.time()
    tour = parallel_processing(sys.argv[1])     
    with open(f'output_{sys.argv[1]}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')
    #print_tour(tour)
    end = time.time()
    print('whole time', end-start)
