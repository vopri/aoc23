from pathlib import Path

# fmt: off
digit_map = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}


def extract_digit_in_line(line, digits, range_: range):
    for i in range_:
        if line[i].isdigit():
            digits.append(line[i])
            break
        for key, value in digit_map.items():
            if line[i:].startswith(key):
                digits.append(value)
                return


def extract_calibration_values_from_line(line: str) -> int:
    digits = []
    extract_digit_in_line(line, digits, range(len(line)))
    extract_digit_in_line(line, digits, range(len(line) - 1, -1, -1))
    return int("".join(digits))


content = Path("input.txt").read_text().splitlines()
print(sum([extract_calibration_values_from_line(line) for line in content]))
