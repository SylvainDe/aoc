# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections
import itertools

resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"


def get_bidded_hand_from_line(string):
    hand, bid = string.split()
    return hand, int(bid)


def get_bidded_hands_from_lines(string):
    return [get_bidded_hand_from_line(l) for l in string.splitlines()]


def get_bidded_hands_from_file(file_path=resource_dir + "year2023_day7_input.txt"):
    with open(file_path) as f:
        return get_bidded_hands_from_lines(f.read())


HIGH_CARD, ONE_PAIR, TWO_PAIR, THREE_OF_A_KIND, FULL_HOUSE, FOUR_OF_A_KIND, FIVE_OF_A_KIND = range(7)

def get_rank(hand):
    c = collections.Counter(hand)
    l = c.most_common()
    (_, mc) = l[0]
    if mc == 5:
        return FIVE_OF_A_KIND
    if mc == 4:
        return FOUR_OF_A_KIND
    if mc == 3:
        (_, mc2) = l[1]
        return FULL_HOUSE if mc2 == 2 else THREE_OF_A_KIND
    if mc == 2:
        (_, mc2) = l[1]
        return TWO_PAIR if mc2 == 2 else ONE_PAIR
    return HIGH_CARD

card_values = dict(zip(reversed('AKQJT98765432'), itertools.count(2)))

def get_sorting_key(bidded_hand):
    hand, bid = bidded_hand
    return get_rank(hand), [card_values[c] for c in hand]

def find_winning(bidded_hands):
    ranks = [get_rank(h) for h, _ in bidded_hands]
    sorted_hands = sorted(bidded_hands, key=lambda bh: get_sorting_key(bh))
    w = 0
    for i, (_, bid) in enumerate(sorted_hands, start=1):
        w += i*bid
    return w

def run_tests():
    bidded_hands = get_bidded_hands_from_lines(
        """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    )
    assert find_winning(bidded_hands) == 6440

def get_solutions():
    bidded_hands = get_bidded_hands_from_file()
    print(find_winning(bidded_hands) == 254024898)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
