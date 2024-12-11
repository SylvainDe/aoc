# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

input_re = (
    "(?P<nb_player>\d+) players; last marble is worth (?P<last_marble>\d+) points"
)


def get_game_config_from_line(string):
    match = re.match(input_re, string)
    d = match.groupdict()
    return int(d["nb_player"]), int(d["last_marble"])


def get_game_config_from_file(file_path=top_dir + "resources/year2018_day9_input.txt"):
    with open(file_path) as f:
        for l in f:
            return get_game_config_from_line(l.strip())


def play_game(nb_player, last_marble):
    circle = [0]
    current_pos = 0
    scores = [0 for _ in range(nb_player)]
    for m in range(1, last_marble + 1):
        if m % 23 == 0:
            pos = (current_pos - 7) % len(circle)
            player = (m - 1) % nb_player
            scores[player] += m + circle.pop(pos)
            current_pos = pos
        else:
            pos = 1 + (current_pos + 1) % len(circle)
            circle.insert(pos, m)
        current_pos = pos
    return max(scores)


def run_tests():
    assert play_game(9, 25) == 32
    nb_player, last_marble = get_game_config_from_line(
        "10 players; last marble is worth 1618 points"
    )
    assert play_game(nb_player, last_marble) == 8317
    nb_player, last_marble = get_game_config_from_line(
        "13 players; last marble is worth 7999 points"
    )
    assert play_game(nb_player, last_marble) == 146373
    nb_player, last_marble = get_game_config_from_line(
        "17 players; last marble is worth 1104 points"
    )
    assert play_game(nb_player, last_marble) == 2764
    nb_player, last_marble = get_game_config_from_line(
        "21 players; last marble is worth 6111 points"
    )
    assert play_game(nb_player, last_marble) == 54718
    nb_player, last_marble = get_game_config_from_line(
        "30 players; last marble is worth 5807 points"
    )
    assert play_game(nb_player, last_marble) == 37305


def get_solutions():
    nb_player, last_marble = get_game_config_from_file()
    print(play_game(nb_player, last_marble) == 408679)
    # To be optimised: print(play_game(nb_player, last_marble * 100))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
