import re
from functools import reduce
from operator import mul
from pathlib import Path

# content = Path("3/test_input.txt").read_text()
content = Path("3/input.txt").read_text()
len_of_line = content.index("\n")
len_of_content = len(content)


def is_part_number_adjacent(part_number: re.Match, gear_idx: int) -> bool:
    first_idx = part_number.start()
    last_idx = part_number.end() - 1
    # left
    if gear_idx - 1 == last_idx:
        return True
    # right
    if gear_idx + 1 == first_idx:
        return True
    # above
    idx_top_left = gear_idx - len_of_line - 2
    if idx_top_left >= first_idx and idx_top_left <= last_idx:
        return True
    if idx_top_left + 1 >= first_idx and idx_top_left + 1 <= last_idx:
        return True
    if idx_top_left + 2 >= first_idx and idx_top_left + 2 <= last_idx:
        return True
    # below
    idx_bottom_left = gear_idx + len_of_line
    if idx_bottom_left >= first_idx and idx_bottom_left <= last_idx:
        return True
    if idx_bottom_left + 1 >= first_idx and idx_bottom_left + 1 <= last_idx:
        return True
    if idx_bottom_left + 2 >= first_idx and idx_bottom_left + 2 <= last_idx:
        return True

    # default
    return False


def get_gear_ratio(gear_idx: int) -> int:
    adjacent_part_numbers: list[int] = []
    for part_number in part_numbers:
        if is_part_number_adjacent(part_number, gear_idx):
            adjacent_part_numbers.append(int(part_number.group()))
    if len(adjacent_part_numbers) > 1:
        return reduce(mul, adjacent_part_numbers, 1)
    return 0


part_numbers = list(re.finditer(r"\d+", content))
gear_idxs = [gear_match.start() for gear_match in re.finditer(r"\*", content)]


print("Part 2:", sum([get_gear_ratio(gear_idx) for gear_idx in gear_idxs]))
