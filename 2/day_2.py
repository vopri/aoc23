import re
from functools import reduce
from operator import mul
from pathlib import Path


def evaluate_possible_game(game_str: str) -> int:
    game_name, game = game_str.split(": ")
    for game_set in game.split("; "):
        if not is_game_set_valid(game_set):
            return 0
    return int(game_name.split()[1])


def is_game_set_valid(game_set: str) -> bool:
    colors = game_set.split(", ")
    for color in colors:
        amount, color_string = color.split()
        if color_string == "blue":
            if int(amount) > 14:
                return False
            else:
                continue
        elif color_string == "red":
            if int(amount) > 12:
                return False
            else:
                continue
        elif color_string == "green":
            if int(amount) > 13:
                return False
            else:
                continue
        else:
            raise RuntimeError("unexpected")
    return True


def power_of_cubes(line: str) -> int:
    pattern = r"(\d+) (\w+)"
    colours = {}
    for amount, colour in re.findall(pattern, line):
        amount = int(amount)
        if colour not in colours or colours[colour] < amount:
            colours[colour] = amount
    return reduce(mul, colours.values(), 1)


content = Path("input.txt").read_text()
print("Part 1:", sum([evaluate_possible_game(game) for game in content.splitlines()]))
print("Part 2:", sum([power_of_cubes(game) for game in content.splitlines()]))
