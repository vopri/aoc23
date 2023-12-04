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
matching_no_count: dict[int, int] = dict()  # part 2

with open(input_file) as content:
    for card_id, line in enumerate(content, 1):
        winning_numbers, your_numbers = parse_card(line)
        your_winning_numbers = find_winning_your_winning_numbers(
            winning_numbers, your_numbers
        )
        matching_no_count[card_id] = len(your_winning_numbers)  # part 2
        points_of_cart = evaluate_winning_points(your_winning_numbers)
        points.append(points_of_cart)
print("Part 1:", sum(points))

# part 2
evaluated_cards: dict[int, int] = {}
for card_id in reversed(matching_no_count.keys()):
    if matching_no_count[card_id] == 0:
        evaluated_cards[card_id] = 1
    else:
        counter = 1
        for i in range(card_id + 1, card_id + matching_no_count[card_id] + 1):
            counter += evaluated_cards[i]
            evaluated_cards[card_id] = counter
print("Part 2:", sum(evaluated_cards.values()))
