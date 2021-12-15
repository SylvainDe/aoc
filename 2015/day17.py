# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections


def get_containers_from_file(file_path="day17_input.txt"):
    with open(file_path) as f:
        return [int(l.strip()) for l in f]


def get_nb_ways(volume, containers):
    ways = collections.Counter([volume])
    for c in sorted(containers):
        for vol, count in list(ways.items()):
            vol2 = vol - c
            if vol2 >= 0:
                ways[vol2] += count
    return ways[0]


def get_nb_ways2(volume, containers):
    ways = collections.Counter([(volume, 0)])
    for c in sorted(containers):
        for (rem_vol, nb_container), count in list(ways.items()):
            vol2 = rem_vol - c
            if vol2 >= 0:
                ways[(vol2, nb_container + 1)] += count
    min_cont = min(
        nb_container for rem_vol, nb_container in ways.keys() if rem_vol == 0
    )
    return ways[(0, min_cont)]


def run_tests():
    assert get_nb_ways(25, [20, 15, 10, 5, 5]) == 4
    assert get_nb_ways2(25, [20, 15, 10, 5, 5]) == 3


def get_solutions():
    containers = get_containers_from_file()
    print(get_nb_ways(150, containers))
    print(get_nb_ways2(150, containers))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
