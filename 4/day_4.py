def parse_card(line: str):
    winning_numbers, your_numbers = line.split(": ")[1].split(" | ")
    winning_numbers = [int(no) for no in winning_numbers.split()]
    your_numbers = [int(no) for no in your_numbers.split()]
    return winning_numbers, your_numbers


def find_winning_your_winning_numbers(
    winning_numbers: list[int], your_numbers: list[int]
) -> list[int]:
    your_winning_numbers = []
    for no in your_numbers:
        if no in winning_numbers:
            your_winning_numbers.append(no)
            winning_numbers.remove(no)
    return your_winning_numbers


def evaluate_winning_points(your_winning_numbers: list[int]) -> int:
    amount = len(your_winning_numbers)
    if amount == 0:
        return 0
    elif amount == 1:
        return 1
    else:
        return 2 ** (amount - 1)


input_file = "4/test_input.txt"
input_file = "4/input.txt"
points: list[int] = []
with open(input_file) as content:
    for line in content:
        winning_numbers, your_numbers = parse_card(line)
        your_winning_numbers = find_winning_your_winning_numbers(
            winning_numbers, your_numbers
        )
        points_of_cart = evaluate_winning_points(your_winning_numbers)
        points.append(points_of_cart)
print("Part 1:", sum(points))
