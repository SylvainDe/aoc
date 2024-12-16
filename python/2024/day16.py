# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_map_content_from_lines(string):
    walls = set()
    start, end = None, None
    for i, l in enumerate(string.splitlines()):
        for j, v in enumerate(l):
            pos = i, j
            if v == '#':
                walls.add(pos)
            elif v == 'S':
                start = pos
            elif v == 'E':
                end = pos
            else:
                assert v == '.'
    return start, end, walls

def get_map_content_from_file(file_path=top_dir + "resources/year2024_day16_input.txt"):
    with open(file_path) as f:
        return get_map_content_from_lines(f.read())


def get_path(map_content):
    start, end, walls = map_content
    dist = dict()

def run_tests():
    map_content = get_map_content_from_lines(
        """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""
    )
    print(get_path(map_content))


def get_solutions():
    map_content = get_map_content_from_file()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
