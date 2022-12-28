# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools
import collections


def get_point_from_line(string):
    return tuple(int(s) for s in string.split(","))


def get_points_from_lines(string):
    return [get_point_from_line(l) for l in string.splitlines()]


def get_points_from_file(file_path="../../resources/year2018_day25_input.txt"):
    with open(file_path) as f:
        return get_points_from_lines(f.read())


def manhattan(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))


def get_nb_constellations(points):
    # Compute close points
    close_pairs = [
        (i1, i2)  # Work with indices because we do not need the actual values
        for ((i1, p1), (i2, p2)) in itertools.combinations(enumerate(points), 2)
        if manhattan(p1, p2) <= 3
    ]
    # Compute adjacency matrix
    links = dict()
    for a, b in close_pairs:
        links.setdefault(a, set()).add(b)
        links.setdefault(b, set()).add(a)
    # Compute connected components
    points = [i for i, p in enumerate(points)]
    connected_points = set()
    components = []
    for p in points:
        if p not in connected_points:
            comp = set()
            queue = collections.deque([p])
            while queue:
                p2 = queue.popleft()
                if p2 in comp:
                    continue
                comp.add(p2)
                assert p2 not in connected_points
                queue.extend(links.get(p2, set()) - comp)
            components.append(comp)
            connected_points.update(comp)
    return len(components)


def run_tests():
    points = get_points_from_lines(
        """0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0"""
    )
    assert get_nb_constellations(points) == 2
    points = get_points_from_lines(
        """-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0"""
    )
    assert get_nb_constellations(points) == 4
    points = get_points_from_lines(
        """1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2"""
    )
    assert get_nb_constellations(points) == 3
    points = get_points_from_lines(
        """1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2"""
    )
    assert get_nb_constellations(points) == 8


def get_solutions():
    points = get_points_from_file()
    print(get_nb_constellations(points) == 338)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
