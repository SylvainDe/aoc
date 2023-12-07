# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_groups_from_file(file_path=top_dir + "resources/year2020_day6_input.txt"):
    with open(file_path) as f:
        return get_groups_from_string(f.read())


def get_groups_from_string(string):
    return [s.split() for s in string.split("\n\n")]


def get_sum_of_any_yes_answers(groups):
    return sum(len(set("".join(g))) for g in groups)


def get_sum_of_all_yes_answers(groups):
    return sum(len(set(g[0]).intersection(*g)) for g in groups)


def run_tests():
    example1 = """abc

a
b
c

ab
ac

a
a
a
a

b"""
    groups = get_groups_from_string(example1)
    assert get_sum_of_any_yes_answers(groups) == 11
    assert get_sum_of_all_yes_answers(groups) == 6


def get_solutions():
    groups = get_groups_from_file()
    print(get_sum_of_any_yes_answers(groups) == 6416)
    print(get_sum_of_all_yes_answers(groups) == 3050)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
