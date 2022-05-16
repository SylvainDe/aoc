# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import itertools
import collections

scanner_re = r"^--- scanner (\d+) ---$"


def get_info_from_lines(lines):
    scanner = None
    info = []
    scanner_info = []
    for l in lines:
        if scanner is None:
            m = re.match(scanner_re, l)
            scanner = int(m.group(1))
            assert scanner == len(info)
        elif l == "":
            info.append(tuple(scanner_info))
            scanner = None
            scanner_info = []
        else:
            pos = tuple(int(v) for v in l.split(","))
            scanner_info.append(pos)
    assert scanner_info
    info.append(tuple(scanner_info))
    return info


def get_info_from_file(file_path="day19_input.txt"):
    with open(file_path) as f:
        return get_info_from_lines([l.strip() for l in f])


def gap(p1, p2):
    # Compute some tuple representing the gap between 2 points
    # That value does not depend on the position/orientation of the observer
    return tuple(sorted(abs(c1 - c2) for c1, c2 in zip(p1, p2)))


def raw_gap(p1, p2):
    return tuple((c1 - c2) for c1, c2 in zip(p1, p2))


def manhattan(p1, p2):
    return sum(abs(c1 - c2) for c1, c2 in zip(p1, p2))


def get_gaps(info):
    # Mapping gaps to list of (scanner number, beacon1, beacon2)
    gaps = dict()
    for i, scanner_info in enumerate(info):
        for (b1, p1), (b2, p2) in itertools.combinations(enumerate(scanner_info), 2):
            gaps.setdefault(gap(p1, p2), []).append((i, b1, b2))
    return gaps


def get_overlaps(gaps, nb_common):
    # If scanners have n overlapping points, we expect n*(n-1)/2
    # common pairs of points seen from the 2 scanners
    nb_overlaps = nb_common * (nb_common - 1) // 2
    # Count similar gaps for each pair of scanners
    overlaps = collections.Counter()
    for gap, points in gaps.items():
        for p1, p2 in itertools.combinations(points, 2):
            i, _, _ = p1
            j, _, _ = p2
            k = tuple(sorted([i, j]))
            overlaps[k] += 1
    graph = dict()
    for (s1, s2), count in overlaps.items():
        if count >= nb_overlaps:
            graph.setdefault(s1, []).append(s2)
            graph.setdefault(s2, []).append(s1)
    return graph


def get_rotations():
    for s_x, s_y, s_z in itertools.product([-1, 1], repeat=3):
        yield lambda x, y, z: (s_x * x, s_y * y, s_z * z)
        yield lambda x, y, z: (s_x * x, s_z * z, s_y * y)
        yield lambda x, y, z: (s_y * y, s_x * x, s_z * z)
        yield lambda x, y, z: (s_y * y, s_z * z, s_x * x)
        yield lambda x, y, z: (s_z * z, s_y * y, s_x * x)
        yield lambda x, y, z: (s_z * z, s_x * x, s_y * y)


def convert_scanner_info(reference_points, scanner_info, nb_common):
    # If scanners have n overlapping points, we expect n*(n-1) similar gaps
    nb_overlaps = nb_common * (nb_common - 1)
    ref_raw_gaps = set(
        raw_gap(p1, p2) for p1, p2 in itertools.permutations(reference_points, 2)
    )
    for rot in get_rotations():
        info = [rot(*point) for point in scanner_info]
        raw_gaps = set(raw_gap(p1, p2) for p1, p2 in itertools.permutations(info, 2))
        nb_match = len(raw_gaps.intersection(ref_raw_gaps))
        if nb_match >= nb_overlaps:
            deltas = collections.Counter(
                raw_gap(p1, p2) for p1, p2 in itertools.product(reference_points, info)
            )
            delta, count = deltas.most_common(1)[0]
            if count >= nb_common:
                dx, dy, dz = delta
                info = [(x + dx, y + dy, z + dz) for x, y, z in info]
                assert len(set(info).intersection(set(reference_points))) >= nb_common
                return info, delta
    assert False


def convert_points(info, nb_common):
    gaps = get_gaps(info)
    overlaps = get_overlaps(gaps, nb_common)
    scanners = set(range(len(info)))
    assert scanners == set(overlaps.keys())
    # Assume scanner 0 is the reference and convert everything into it
    # Map index to tuple (list of points, position of scanner)
    converted = {0: (info[0], (0, 0, 0))}
    change = True
    while change:
        change = False
        for scan in scanners:
            for neigh in overlaps[scan]:
                if scan not in converted and neigh in converted:
                    converted[scan] = convert_scanner_info(
                        converted[neigh][0], info[scan], nb_common
                    )
                    change = True
    assert all(s in converted for s in scanners)
    all_points = set()
    for (points, scanner) in converted.values():
        all_points.update(points)
    all_scanners = [scanner for points, scanner in converted.values()]
    return all_points, all_scanners


def get_max_distance(points):
    return max(manhattan(p1, p2) for p1, p2 in itertools.combinations(points, 2))


def run_tests():
    nb_common = 12
    info = get_info_from_file("day19_example_input.txt")
    gaps = get_gaps(info)
    overlaps = get_overlaps(gaps, nb_common)
    assert 1 in overlaps[0]
    assert 0 in overlaps[1]
    assert 1 in overlaps[4]
    assert 4 in overlaps[1]
    converted_points, converted_scanners = convert_points(info, nb_common)
    assert len(converted_points) == 79
    assert get_max_distance(converted_scanners) == 3621


def get_solutions():
    nb_common = 12
    info = get_info_from_file()
    converted_points, converted_scanners = convert_points(info, nb_common)
    print(len(converted_points))
    print(get_max_distance(converted_scanners))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
