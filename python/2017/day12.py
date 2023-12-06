# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"


def get_connection_list_from_line(string):
    sep1, sep2 = " <-> ", ", "
    left, mid, right = string.partition(sep1)
    assert mid == sep1
    return (int(left), tuple(int(c) for c in right.split(sep2)))


def get_connection_list_from_lines(string):
    return [get_connection_list_from_line(l) for l in string.splitlines()]


def get_connection_list_from_file(file_path=resource_dir + "year2017_day12_input.txt"):
    with open(file_path) as f:
        return get_connection_list_from_lines(f.read())


def get_connection_matrix(connection_list):
    connection_dict = dict()
    for id1, ids in connection_list:
        for id2 in ids:
            connection_dict.setdefault(id1, set()).add(id2)
            connection_dict.setdefault(id2, set()).add(id1)
    return connection_dict


def get_group(connection_dict, identifier):
    group = set()
    new_elts = [identifier]
    while new_elts:
        elt = new_elts.pop()
        if elt not in group:
            group.add(elt)
            new_elts.extend(connection_dict[elt] - group)
    return group


def part1(connection_list, identifier=0):
    connection_dict = get_connection_matrix(connection_list)
    return len(get_group(connection_dict, identifier))


def part2(connection_list):
    connection_dict = get_connection_matrix(connection_list)
    grouped = set()
    nb_group = 0
    for iden in connection_dict:
        if iden not in grouped:
            nb_group += 1
            for iden2 in get_group(connection_dict, iden):
                assert iden2 not in grouped
                grouped.add(iden2)
    return nb_group


def run_tests():
    connection_list = get_connection_list_from_lines(
        """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
    )
    assert part1(connection_list) == 6
    assert part2(connection_list) == 2


def get_solutions():
    connection_list = get_connection_list_from_file()
    print(part1(connection_list) == 115)
    print(part2(connection_list) == 221)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
