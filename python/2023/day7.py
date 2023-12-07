# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections
import itertools

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_bidded_hand_from_line(string):
    hand, bid = string.split()
    return hand, int(bid)


def get_bidded_hands_from_lines(string):
    return [get_bidded_hand_from_line(l) for l in string.splitlines()]


def get_bidded_hands_from_file(file_path=top_dir + "resources/year2023_day7_input.txt"):
    with open(file_path) as f:
        return get_bidded_hands_from_lines(f.read())


HIGH_CARD, ONE_PAIR, TWO_PAIR, THREE_OF_A_KIND, FULL_HOUSE, FOUR_OF_A_KIND, FIVE_OF_A_KIND = range(7)

def get_rank(hand, use_joker):
    c = collections.Counter(hand)
    if use_joker:
        nb_joker = c['J']
        c['J'] = 0
    else:
        nb_joker = 0
    l = [nb for _, nb in c.most_common()]
    mc = l[0] + nb_joker
    if mc == 5:
        return FIVE_OF_A_KIND
    if mc == 4:
        return FOUR_OF_A_KIND
    if mc == 3:
        return FULL_HOUSE if l[1] == 2 else THREE_OF_A_KIND
    if mc == 2:
        return TWO_PAIR if l[1] == 2 else ONE_PAIR
    return HIGH_CARD

card_values_no_joker = dict(zip(reversed('AKQJT98765432'), itertools.count(2)))
card_values_with_joker = dict(zip(reversed('AKQT98765432J'), itertools.count(2)))

def get_sorting_key(hand, use_joker):
    card_values = card_values_with_joker if use_joker else card_values_no_joker
    return get_rank(hand, use_joker), [card_values[c] for c in hand]

def find_winning(bidded_hands, use_joker):
    sorted_hands = sorted(bidded_hands, key=lambda bh: get_sorting_key(bh[0], use_joker))
    return sum(i * bid
               for i, (_, bid) in enumerate(sorted_hands, start=1))

def run_tests():
    bidded_hands = get_bidded_hands_from_lines(
        """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    )
    assert find_winning(bidded_hands, False) == 6440
    assert find_winning(bidded_hands, True) == 5905

def get_solutions():
    bidded_hands = get_bidded_hands_from_file()
    print(find_winning(bidded_hands, False) == 254024898)
    print(find_winning(bidded_hands, True) == 254115617)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
