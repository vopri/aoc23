from pathlib import Path


def get_first_digit_value(line: str) -> str:
    for char in line:
        if char.isdigit():
            return char
    raise RuntimeError("end of line")


def extract_value_from_line(line: str) -> int:
    line = handle_literal_digits(line)
    first_digit_in_line = get_first_digit_value(line)
    last_digit_in_line = get_first_digit_value(line[::-1])
    return int(first_digit_in_line + last_digit_in_line)


def get_calibration_value(content: str) -> int:
    return sum([extract_value_from_line(line.strip()) for line in content.splitlines()])


def handle_literal_digits(line: str) -> str:
    digits = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    def insert_digit(line: str, forward: bool = True) -> str:
        if forward:
            idxs = range(len(line))
        else:
            idxs = range(len(line))[::-1]
        for i in idxs:
            subline = line[i:]
            for key, value in digits.items():
                if subline.startswith(key):
                    return line[:i] + value + line[i:]
        return line

    line = insert_digit(line, forward=True)
    line = insert_digit(line, forward=False)
    return line


content = Path("input.txt").read_text()
print(f"{get_calibration_value(content)=}")
