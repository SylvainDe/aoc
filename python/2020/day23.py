# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"


RUN_LONG_TESTS = False


def get_cups_from_file(file_path=resource_dir + "year2020_day23_input.txt"):
    with open(file_path) as f:
        for l in f:
            return [int(c) for c in l.strip()]


def init_linked_dict(lst):
    beg = lst[0]
    linked_dict = dict(zip(lst, lst[1:] + [beg]))
    return beg, linked_dict


def remove_from_linked_dict(linked_dict, rm_after):
    removed = linked_dict[rm_after]
    linked_dict[rm_after] = linked_dict.pop(removed)
    return removed


def insert_in_linked_dict(linked_dict, insert_after, value):
    after = linked_dict[insert_after]
    linked_dict[insert_after] = value
    linked_dict[value] = after


def perform_move_with_linked_dict(cup_dict, curr):
    min_cup, max_cup = 1, len(cup_dict)
    nb_removed = 3
    removed = []
    for _ in range(nb_removed):
        removed.append(remove_from_linked_dict(cup_dict, curr))
    dest = curr - 1
    while dest not in cup_dict:
        if dest < min_cup:
            dest = max_cup
        else:
            dest -= 1
    for c in reversed(removed):
        insert_in_linked_dict(cup_dict, dest, c)
    return cup_dict, cup_dict[curr]


def perform_moves(cups, nb):
    curr, cup_dict = init_linked_dict(cups)
    for _ in range(nb):
        cup_dict, curr = perform_move_with_linked_dict(cup_dict, curr)
    return cup_dict


def day1(cups, nb=100):
    cup_dict = perform_moves(cups, nb)
    ret = []
    curr = 1
    while cup_dict[curr] != 1:
        curr = cup_dict[curr]
        ret.append(curr)
    return int("".join(str(c) for c in ret))


def day2(cups, nb_cups=1000000, nb_iter=10000000):
    all_cups = cups + list(range(max(cups) + 1, nb_cups + 1))
    cup_dict = perform_moves(all_cups, nb_iter)
    n1 = cup_dict[1]
    n2 = cup_dict[n1]
    return n1 * n2


def run_tests():
    example1 = "389125467"
    cups = [int(c) for c in example1]
    assert day1(cups, 10) == 92658374
    assert day1(cups) == 67384529
    if RUN_LONG_TESTS:
        assert day2(cups) == 149245887792


def get_solutions():
    cups = get_cups_from_file()
    print(day1(cups) == 96342875)
    if RUN_LONG_TESTS:
        print(day2(cups) == 563362809504)


if __name__ == "__main__":
    RUN_LONG_TESTS = True
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
