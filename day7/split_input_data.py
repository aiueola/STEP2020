#!/usr/bin/env python3

import sys
import math

from common import print_tour, read_input

# this writes each data in different csv_file
def write_new_data(filename, cities):
    with open(filename, 'w') as f:
        f.write('x,y,index\n')
        for x, y, index in cities:
            f.write(f'{x},{y},{index}\n')

# this module split areas to four domain
def split_data(file_num):
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
    
    # write to four different csv_files
    write_new_data('input_{}_{}.csv'.format(file_num, 'upper_left'), upper_left)
    write_new_data('input_{}_{}.csv'.format(file_num, 'upper_right'), upper_right)
    write_new_data('input_{}_{}.csv'.format(file_num, 'bottom_left'), bottom_left)
    write_new_data('input_{}_{}.csv'.format(file_num, 'bottom_right'), bottom_right)
    

if __name__ == '__main__':
    # command should be: python split_input_data.py 6(or7)
    # if you want to test in small data, 0-5 also works for parse
    # this number means which input to use, not split size.
    assert len(sys.argv) > 1
    split_data(sys.argv[1])
