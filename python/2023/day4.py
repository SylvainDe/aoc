# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

CARD_RE = re.compile(r"Card +(\d+): (.*) \| (.*)")


def get_card_from_line(string):
    m = CARD_RE.match(string)
    card_id, numbers, winning = m.groups()
    return (
        int(card_id),
        [int(s) for s in numbers.split()],
        [int(s) for s in winning.split()],
    )


def get_cards_from_lines(string):
    return [get_card_from_line(l) for l in string.splitlines()]


def get_cards_from_file(file_path=top_dir + "resources/year2023_day4_input.txt"):
    with open(file_path) as f:
        return get_cards_from_lines(f.read())


def get_card_score(card):
    _, numbers, winning = card
    n = len(set(numbers).intersection(winning))
    return 2 ** (n - 1) if n else 0


def get_nb_cards(cards):
    cards_to_process = {card_id: 1 for card_id, _, _ in cards}
    for card_id, numbers, winning in cards:
        nb = cards_to_process[card_id]
        nb_win = len(set(numbers).intersection(winning))
        for c2 in range(card_id + 1, card_id + nb_win + 1):
            cards_to_process[c2] += nb
    return sum(cards_to_process.values())


def run_tests():
    cards = get_cards_from_lines(
        """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    )
    assert sum(get_card_score(c) for c in cards) == 13
    assert get_nb_cards(cards) == 30


def get_solutions():
    cards = get_cards_from_file()
    print(sum(get_card_score(c) for c in cards) == 23441)
    print(get_nb_cards(cards) == 5923918)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
