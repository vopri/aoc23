from itertools import pairwise
from typing import TypeAlias

DataSets: TypeAlias = list[list[int]]


def prepare_data(data_sets: DataSets, data_set: list[int]) -> DataSets:
    data_sets.append(data_set)
    if all(data == 0 for data in data_set):
        return data_sets
    else:
        data_set = [b - a for a, b in pairwise(data_set)]
        return prepare_data(data_sets, data_set)


def evaluate_data(data_sets: DataSets) -> int:
    data_sets = list(reversed(data_sets))
    value = 0
    for data in data_sets:
        data.append(data[-1] + value)
        value = data[-1]
    return value


def extrapolate_next_value(values: list[int]) -> int:
    data_sets = prepare_data([], values)
    return evaluate_data(data_sets)


def parse_line(line: str):
    return [int(char) for char in line.split()]


file = "9/test_input.txt"
file = "9/input.txt"
with open(file) as file:
    extrapolate_values = [extrapolate_next_value(parse_line(line)) for line in file]
print("Part 1:", sum(extrapolate_values))
