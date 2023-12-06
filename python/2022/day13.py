# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import functools
import ast


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

def get_packets_from_line(string):
    return tuple(ast.literal_eval(s) for s in string.split("\n"))


def get_packets_from_lines(string):
    return [get_packets_from_line(l.strip()) for l in string.split("\n\n")]


def get_packets_from_file(file_path=resource_dir + "year2022_day13_input.txt"):
    with open(file_path) as f:
        return get_packets_from_lines(f.read())


def cmp_func(p1, p2):
    t1, t2 = type(p1), type(p2)
    if (t1, t2) == (int, int):
        if p1 != p2:
            return 1 if p1 < p2 else -1
    elif (t1, t2) == (list, list):
        for v1, v2 in zip(p1, p2):
            order = cmp_func(v1, v2)
            if order != 0:
                return order
        l1, l2 = len(p1), len(p2)
        if l1 != l2:
            return 1 if l1 < l2 else -1
    elif (t1, t2) == (list, int):
        return cmp_func(p1, [p2])
    elif (t1, t2) == (int, list):
        return cmp_func([p1], p2)
    return 0


def part1(packets):
    return sum(i for (i, pair) in enumerate(packets, start=1) if cmp_func(*pair) == 1)


def part2(packets):
    div1, div2 = (ast.literal_eval(p) for p in ("[[2]]", "[[6]]"))
    all_packets = [div1, div2]
    for pair in packets:
        all_packets.extend(pair)
    sorted_packets = sorted(
        all_packets, key=functools.cmp_to_key(cmp_func), reverse=True
    )
    return (1 + sorted_packets.index(div1)) * (1 + sorted_packets.index(div2))


def run_tests():
    packets = get_packets_from_lines(
        """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
    )
    assert part1(packets) == 13
    assert part2(packets) == 140


def get_solutions():
    packets = get_packets_from_file()
    print(part1(packets) == 5185)
    print(part2(packets) == 23751)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
