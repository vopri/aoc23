import re
from functools import reduce
from operator import mul
from pathlib import Path

# content = Path("3/test_input.txt").read_text()
content = Path("3/input.txt").read_text()
len_of_line = content.index("\n")


def is_part_number_adjacent(part_number: re.Match, gear_idx: int) -> bool:
    first_idx_part_no = part_number.start()
    last_idx_part_no = part_number.end() - 1
    # check left of gear
    if gear_idx - 1 == last_idx_part_no:
        return True
    # check right of gear
    if gear_idx + 1 == first_idx_part_no:
        return True

    def scan_left_to_right(start_index: int) -> bool:
        if start_index >= first_idx_part_no and start_index <= last_idx_part_no:
            return True
        if start_index + 1 >= first_idx_part_no and start_index + 1 <= last_idx_part_no:
            return True
        if start_index + 2 >= first_idx_part_no and start_index + 2 <= last_idx_part_no:
            return True
        return False

    # check above gear
    idx_top_left = gear_idx - len_of_line - 2
    if scan_left_to_right(idx_top_left):
        return True
    # check below gear
    idx_bottom_left = gear_idx + len_of_line
    if scan_left_to_right(idx_bottom_left):
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
