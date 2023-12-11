from collections import deque
from itertools import pairwise
from typing import TypeAlias

DataSets: TypeAlias = list[deque[int]]


def prepare_data(data_sets: DataSets, data_set: deque[int], part_1: bool) -> DataSets:
    data_sets.append(data_set)
    if all(data == 0 for data in data_set):
        return data_sets
    else:
        if part_1:
            data_set = deque([b - a for a, b in pairwise(data_set)])
        else:
            data_set = deque([a - b for a, b in pairwise(data_set)])

        return prepare_data(data_sets, data_set, part_1)


def evaluate_data(data_sets: DataSets, part_1) -> int:
    data_sets = list(reversed(data_sets))
    value = 0
    for data in data_sets:
        if part_1:
            data.append(data[-1] + value)
            value = data[-1]
        else:
            data.appendleft(data[0] + value)
            value = data[0]
    return value


def extrapolate_next_value(values: deque[int], part_1: bool = True) -> int:
    data_sets = prepare_data([], values, part_1)
    return evaluate_data(data_sets, part_1)


def parse_line(line: str) -> deque:
    return deque([int(char) for char in line.split()])


file = "9/test_input.txt"
file = "9/input.txt"
with open(file) as file:
    extrapolate_values_part_1 = []
    extrapolate_values_part_2 = []
    for line in file:
        extrapolate_values_part_1.append(extrapolate_next_value(parse_line(line)))
        extrapolate_values_part_2.append(
            extrapolate_next_value(parse_line(line), part_1=False)
        )

print("Part 1:", sum(extrapolate_values_part_1))
print("Part 2:", sum(extrapolate_values_part_2))
