import re
from pathlib import Path

# content = Path("3/test_input.txt").read_text()
content = Path("3/input.txt").read_text()
len_of_line = content.index("\n")
len_of_content = len(content)
irrelavnt_symobls = (".", "\n")


def is_symbol_before_match(match_: re.Match) -> bool:
    if match_.start() > 0 and content[match_.start() - 1] not in irrelavnt_symobls:
        return True
    return False


def is_symbol_after_match(match_: re.Match) -> bool:
    if (
        match_.end() < len_of_content - 1
        and content[match_.end()] not in irrelavnt_symobls
    ):
        return True
    return False


def is_symbol_adjacent_prev_line(match_: re.Match) -> bool:
    range_start = match_.start() - len_of_line - 2
    range_end = match_.end() - len_of_line
    if range_start < 0:
        range_start = 0
    if range_end > len_of_content:
        range_end = len_of_content
    for i in range(range_start, range_end):
        if content[i] not in irrelavnt_symobls:
            return True
    return False


def is_symbol_adjacent_next_line(match_: re.Match) -> bool:
    range_start = match_.start() + len_of_line
    range_end = match_.end() + len_of_line + 2
    for i in range(range_start, range_end):
        try:
            if content[i] not in irrelavnt_symobls:
                return True
        except IndexError:
            pass
    return False


def is_adjacent_to_symbol(match_: re.Match) -> bool:
    if is_symbol_before_match(match_):
        return True
    if is_symbol_after_match(match_):
        return True
    if is_symbol_adjacent_prev_line(match_):
        return True
    if is_symbol_adjacent_next_line(match_):
        return True
    return False


part_numbers = []
for match_ in re.finditer(r"\d+", content):
    if is_adjacent_to_symbol(match_):
        part_numbers.append(int(match_.group()))
print("Part 1:", sum(part_numbers))
