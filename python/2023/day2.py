# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import collections

GAME_RE = re.compile(r"Game (\d+): (.*)")


def get_nb_and_color(s):
    nb, color = s.split(" ")
    return int(nb), color


def get_game_from_line(string):
    m = GAME_RE.match(string)
    game_id, cube_list_str = m.groups()
    subsets = []
    for s1 in cube_list_str.split("; "):
        subsets.append([get_nb_and_color(s2) for s2 in s1.split(", ")])
    return int(game_id), subsets


def get_games_from_lines(string):
    return [get_game_from_line(l) for l in string.splitlines()]


def get_games_from_file(file_path="../../resources/year2023_day2_input.txt"):
    with open(file_path) as f:
        return get_games_from_lines(f.read())


def is_valid(subsets, bag):
    return all(nb <= bag[color] for subset in subsets for nb, color in subset)


def part1(games):
    bag = {'red': 12, 'green': 13, 'blue': 14}
    return sum(game_id for game_id, subsets in games if is_valid(subsets, bag))


def smallest_set(subsets):
    smallest_set = collections.Counter()
    for subset in subsets:
        for nb, color in subset:
            smallest_set[color] = max(smallest_set[color], nb)
    return smallest_set['blue'] * smallest_set['green'] * smallest_set['red']


def part2(games):
    return sum(smallest_set(subsets) for game_id, subsets in games)


def run_tests():
    games = get_games_from_lines(
        """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    )
    assert part1(games) == 8
    assert part2(games) == 2286


def get_solutions():
    games = get_games_from_file()
    print(part1(games) == 3059)
    print(part2(games) == 65371)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
