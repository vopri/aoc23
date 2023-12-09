from itertools import cycle
from math import lcm
from pathlib import Path
from typing import Iterable, Iterator, TypeAlias

Tree: TypeAlias = dict[str, tuple[str, str]]


def parse(file: str) -> tuple[Iterator[str], Tree]:
    content = Path(file).read_text().splitlines()
    instructions = cycle(content[0].strip())
    tree: Tree = dict()
    for line in content[2:]:
        key, value = line.split(" = ")
        left, right = value.strip(" ()").split(", ")
        tree[key] = left, right
    return instructions, tree


file = "8/input.txt"
instructions, tree = parse(file)


def count_steps(start_point: str, stop_condition) -> int:
    steps = 0
    current_position = start_point
    while not stop_condition(current_position):
        next_step = next(instructions)
        steps += 1
        if next_step == "L":
            current_position = tree[current_position][0]
        else:
            current_position = tree[current_position][1]
    return steps


print(
    "Part 1:",
    count_steps(start_point="AAA", stop_condition=lambda cur_pos: cur_pos == "ZZZ"),
)
# part 2
starting_points = [key for key in tree.keys() if key.endswith("A")]
path_lenghts = [
    count_steps(start_point, lambda cur_pos: cur_pos.endswith("Z"))
    for start_point in starting_points
]
print("Part 2:", lcm(*path_lenghts))
