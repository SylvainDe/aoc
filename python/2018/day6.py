# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools
import collections


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_location_from_line(string):
    return tuple(int(c) for c in string.split(", "))


def get_locations_from_lines(string):
    return [get_location_from_line(l) for l in string.splitlines()]


def get_locations_from_file(file_path=top_dir + "resources/year2018_day6_input.txt"):
    with open(file_path) as f:
        return get_locations_from_lines(f.read())


def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def get_biggest_area(locations):
    areas = collections.Counter()
    infinite_areas = set()
    # Get bounding box
    xs = [p[0] for p in locations]
    ys = [p[1] for p in locations]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    for p in itertools.product(range(x_min, x_max + 1), range(y_min, y_max + 1)):
        distances = dict()
        for p2 in locations:
            distances.setdefault(distance(p, p2), []).append(p2)
        d_min = min(distances.keys())
        lst_min = distances[d_min]
        if len(lst_min) == 1:
            p_min = lst_min[0]
            areas[p_min] += 1
            if p[0] in (x_min, x_max) or p[1] in (y_min, y_max):
                infinite_areas.add(p_min)
    return max(area for point, area in areas.items() if point not in infinite_areas)


def get_size_of_regions_total_distance_less_than(locations, limit):
    area = 0
    # Get bounding box - TODO this should probably be done in a smarter way
    # because I do not see any reason why every relevant point would be in it
    xs = [p[0] for p in locations]
    ys = [p[1] for p in locations]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    for p in itertools.product(range(x_min, x_max + 1), range(y_min, y_max + 1)):
        total_dist = sum(distance(p, p2) for p2 in locations)
        if total_dist < limit:
            area += 1
    return area


def run_tests():
    locations = get_locations_from_lines(
        """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""
    )
    assert get_biggest_area(locations) == 17
    assert get_size_of_regions_total_distance_less_than(locations, 32) == 16


def get_solutions():
    locations = get_locations_from_file()
    print(get_biggest_area(locations) == 4186)
    print(get_size_of_regions_total_distance_less_than(locations, 10000) == 45509)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
