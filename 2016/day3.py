# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_triangle_from_line(line):
    return tuple(int(v) for v in line.split())


def get_triangles_from_file(file_path="day3_input.txt"):
    with open(file_path) as f:
        return [get_triangle_from_line(l.strip()) for l in f]


def triangle_is_possible(t):
    a, b, c = sorted(t)
    return a + b > c


def run_tests():
    assert not triangle_is_possible((5, 10, 25))
    assert triangle_is_possible((5, 10, 12))


def get_solutions():
    triangles = get_triangles_from_file()
    print(sum(triangle_is_possible(t) for t in triangles))

    s = 0
    triangles_iter = iter(triangles)
    while True:
        try:
            l1 = next(triangles_iter)
            l2 = next(triangles_iter)
            l3 = next(triangles_iter)
            for i in (0, 1, 2):
                s += triangle_is_possible((l1[i], l2[i], l3[i]))
        except StopIteration:
            break
    print(s)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
