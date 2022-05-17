# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_decks_from_file(file_path="../../resources/year2020_day22_input.txt"):
    with open(file_path) as f:
        return get_decks_from_string(f.read())


def get_decks_from_string(string):
    return [[int(c) for c in d.splitlines()[1:]] for d in string.split("\n\n")]


def play_game(deck1, deck2):
    deck1, deck2 = list(deck1), list(deck2)
    while deck1 and deck2:
        c1, c2 = deck1.pop(0), deck2.pop(0)
        if c1 > c2:
            deck1.extend([c1, c2])
        elif c2 > c1:
            deck2.extend([c2, c1])
        else:
            assert False
    return get_score_for_final_setup((deck1, deck2))


def play_recursive_game(deck1, deck2):
    seen = set()
    while deck1 and deck2:
        deck_config = tuple(deck1 + [None] + deck2)
        if deck_config in seen:
            return deck1, []
        seen.add(deck_config)
        c1, c2 = deck1.pop(0), deck2.pop(0)
        if c1 <= len(deck1) and c2 <= len(deck2):
            subd1, subd2 = play_recursive_game(deck1[:c1], deck2[:c2])
            assert bool(subd1) + bool(subd2) == 1
            winner_is_1 = bool(subd1)
        else:
            winner_is_1 = c1 > c2
        if winner_is_1:
            deck1.extend([c1, c2])
        else:
            deck2.extend([c2, c1])
    return deck1, deck2


def get_score_for_final_setup(decks):
    deck1, deck2 = decks
    return sum(i * c for i, c in enumerate(reversed(deck1 + deck2), start=1))


def run_tests():
    example1 = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
    deck1, deck2 = get_decks_from_string(example1)
    assert play_game(deck1, deck2) == 306
    assert get_score_for_final_setup(play_recursive_game(deck1, deck2)) == 291
    example2 = """Player 1:
43
19

Player 2:
2
29
14"""
    deck1, deck2 = get_decks_from_string(example2)
    assert get_score_for_final_setup(play_recursive_game(deck1, deck2)) == 105


def get_solutions():
    deck1, deck2 = get_decks_from_file()
    print(play_game(deck1, deck2) == 35397)
    print(get_score_for_final_setup(play_recursive_game(deck1, deck2)) == 31120)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
