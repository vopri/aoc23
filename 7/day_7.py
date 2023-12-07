from collections import Counter, namedtuple

Cards = namedtuple("Cards", "hand bid".split())


def parse(input_file: str) -> list[Cards]:
    with open(input_file) as file:
        cardlists: list[Cards] = []
        for line in file:
            hand, bid = line.split()
            bid = int(bid)
            cardlists.append(Cards(hand, bid))
        return cardlists


def evaluate_type(hand: str, part_2=False) -> int:
    counter = Counter(hand)
    if part_2:
        jokers = counter.get("J", 0)
        key, amount = counter.most_common()[0]
        if key == "J":
            # special case: 'JJJJJ'
            if hand == "JJJJJ":
                return 7
            # special case like 'J6758'
            key, _ = counter.most_common()[1]
        counter[key] += jokers
        counter["J"] -= jokers

    match (sorted(counter.values(), reverse=True)):
        # five of a kind
        case [5, *others]:
            value = 7
        # four of a kind
        case [4, *others]:
            value = 6
        # full house
        case [3, 2, *others]:
            value = 5
        # three of a kind
        case [3, *others]:
            value = 4
        # two pair
        case [2, 2, *others]:
            value = 3
        # one pair
        case [2, 1, *others]:
            value = 2
        case _:
            value = 1
    return value


def evaluate_value(hand: str, part_2=False) -> list[int]:
    """If two hands have got the same type"""
    pictures = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10}
    if part_2:
        pictures["J"] = 1
    card_values = []
    for char in hand:
        if char.isdigit():
            card_values.append(int(char))
        else:
            card_values.append(pictures[char])
    return card_values


def evaluate_strength(hand: str, part_2=False) -> tuple[int, list[int]]:
    return evaluate_type(hand, part_2), evaluate_value(hand, part_2)


input_file = "7/test_input.txt"
input_file = "7/input.txt"

cardlists = parse(input_file)

cardlists.sort(key=lambda card: evaluate_strength(card.hand))
total_winnings = sum([(rank * card.bid) for rank, card in enumerate(cardlists, 1)])
print("Part 1:", total_winnings)

cardlists.sort(key=lambda card: evaluate_strength(card.hand, part_2=True))
total_winnings = sum([(rank * card.bid) for rank, card in enumerate(cardlists, 1)])
print("Part 2:", total_winnings)
