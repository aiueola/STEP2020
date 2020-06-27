#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input, format_tour

# to read from each csv file
def read_tour(filename):
    with open(filename) as f:
        tour = []
        for line in f.readlines()[1:]:  # Ignore the first line.
            tour.append(int(line))
        return tour

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
def concat_data(file_num):
    # first, collect data from four areas
    upper_left = read_tour('output_{}_{}.csv'.format(file_num, 'upper_left'))
    upper_right = read_tour('output_{}_{}.csv'.format(file_num, 'upper_right'))
    bottom_left = read_tour('output_{}_{}.csv'.format(file_num, 'bottom_left'))
    bottom_right = read_tour('output_{}_{}.csv'.format(file_num, 'bottom_right'))

    # find closest tour index
    cities = read_input('input_{}.csv'.format(file_num))
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
    
    
if __name__ == '__main__':
    # command should be: python split_input_data.py 6(or7)
    # if you want to test in small data, 0-5 also works for parse
    # this number means which input to use, not split size.
    assert len(sys.argv) > 1
    tour = concat_data(sys.argv[1])
    # write into output_{i}.csv
    with open(f'output_{sys.argv[1]}.csv', 'w') as f:
        f.write(format_tour(tour) + '\n')
