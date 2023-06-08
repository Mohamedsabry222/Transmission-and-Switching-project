import math
import numpy as np
from math import factorial

# Na values for sectoring
Na_values = [3, 4, 7, 9, 12, 13]

# n60, n120, n180 values for sectoring
n60_values = [2, 1, 1, 1, 1, 1]
n120_values = [3, 2, 2, 2, 2, 2]
n180_values = [4, 3, 3, 3, 3, 3]


def erlang(A, m):
    """Calculate Erlang B formula"""
    L = (A ** m) / factorial(m)
    sum_ = sum([(A ** n) / factorial(n) for n in range(m + 1)])
    block = L / sum_
    return block


def get_acell(block_prob, trunks):
    """Perform binary search to find the minimum offered load with the desired blocking probability"""
    left = 0
    right = 1000

    while True:
        mid = (left + right) / 2
        b = erlang(mid, trunks)
        if abs(b - block_prob) < 0.0001:
            return mid
        elif b > block_prob:
            right = mid
        else:
            left = mid


def find_best_sectoring(blocking_prob, total_slots, slots_per_user, channels_per_cluster, num_subscribers,
                        avg_calls_per_user, avg_call_duration, interference_ratio):
    """Find the best sectoring scheme based on blocking probability"""

    N = (interference_ratio * 6) / 3
    A_user = (avg_calls_per_user / (24 * 60)) * avg_call_duration
    trunk = math.floor((channels_per_cluster / N) * (total_slots / slots_per_user))
    A_cell = get_acell(blocking_prob, trunk)
    no_sub_per_cell = math.floor(A_cell / A_user)
    total_cells = math.ceil(num_subscribers / no_sub_per_cell)

    print("Cells without sectoring:", total_cells)

    WN = []

    Ncalculation = N / 6

    # Find working N for 60 sectoring
    for i in range(len(Na_values)):
        if (Na_values[i] / n60_values[i]) > Ncalculation:
            WN.append(Na_values[i])
            break

    trunk60 = math.floor(((channels_per_cluster / WN[0]) * (total_slots / slots_per_user)) / 6)
    A_cell60 = get_acell(blocking_prob, trunk60)
    no_sub_per_cell60 = math.floor(A_cell60 * 6 / A_user)

    # Find working N for 120 sectoring
    for i in range(len(Na_values)):
        if (Na_values[i] / n120_values[i]) > Ncalculation:
            WN.append(Na_values[i])
            break

    trunk120 = math.floor(((channels_per_cluster / WN[1]) * (total_slots / slots_per_user)) / 3)
    A_cell120 = get_acell(blocking_prob, trunk120)
    no_sub_per_cell120 = math.floor(A_cell120 * 3 / A_user)

    # Find working N for 180 sectoring
    for i in range(len(Na_values)):
        if (Na_values[i] / n180_values[i]) > Ncalculation:
            WN.append(Na_values[i])
            break

    trunk180 = math.floor(((channels_per_cluster / WN[2]) * (total_slots / slots_per_user)) / 2)
    A_cell180 = get_acell(blocking_prob, trunk180)
    no_sub_per_cell180 = math.floor(A_cell180 * 2 / A_user)

    if no_sub_per_cell60 > no_sub_per_cell120:
        if no_sub_per_cell60 > no_sub_per_cell180:
            print("we will use 60 sectoring")
        total_cells = math.ceil(num_subscribers / no_sub_per_cell60)
    elif no_sub_per_cell120 > no_sub_per_cell60:
        if no_sub_per_cell180:
            print("we will use 120 sectoring")
        total_cells = math.ceil(num_subscribers / no_sub_per_cell120)
    else:
        print("we will use 180 sectoring")
        total_cells = math.ceil(num_subscribers / no_sub_per_cell180)

    return total_cells


blocking_probability = 0.001
total_slots = 8
slots_per_user = 2
channels_per_cluster = 125
city_size = 450  # in Km2
num_subscribers = 1000000  # number of subscribers per city
avg_calls_per_user = 10  # calls per day
avg_call_duration = 1  # in minutes
interference_ratio = 6.25

TotalNumOfCells = find_best_sectoring(blocking_probability, total_slots, slots_per_user, channels_per_cluster,
                                      num_subscribers, avg_calls_per_user, avg_call_duration, interference_ratio)
print("Number of cells:", TotalNumOfCells)
