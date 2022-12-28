# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import itertools

# Sensor at x=2, y=18: closest beacon is at x=-2, y=15
sensors_re = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)


def get_sensor_from_line(string):
    sx, sy, bx, by = [int(s) for s in sensors_re.match(string).groups()]
    return (sx, sy), (bx, by)


def get_sensor_from_lines(string):
    return [get_sensor_from_line(l) for l in string.splitlines()]


def get_sensor_from_file(file_path="../../resources/year2022_day15_input.txt"):
    with open(file_path) as f:
        return get_sensor_from_lines(f.read())


def distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def get_pos_without_beacons(sensors, y_arg):
    points = set()
    for s, b in sensors:
        sx, sy = s
        closest = (sx, y_arg)
        d_b = distance(s, b)
        d_closest = distance(s, closest)
        l = d_b - d_closest
        if l >= 0:
            new_points = [(sx + dx, y_arg) for dx in range(-l, l + 1)]
            # for p in new_points:
            #     assert distance(s, p) <= d_b
            points.update(new_points)
    return len(points - set(b for s, b in sensors))


def get_freq(x, y):
    return x * 4000000 + y


def get_pos_with_beacons_naive(sensors, val_max):
    sensors_dist = {s: distance(s, b) for s, b in sensors}
    for p in itertools.product(range(val_max + 1), repeat=2):
        if all(distance(s, p) > d for s, d in sensors_dist.items()):
            return get_freq(*p)


def get_manhattan_circle(center, radius):
    x, y = center
    points = set()
    for i in range(radius + 1):
        # Note: tiny overlap which could probably be optimised with better code
        points.add((i + x, y + radius - i))  # upper-right
        points.add((i + x, y - radius + i))  # upper-left
        points.add((i + x - radius, y + i))  # lower-right
        points.add((i + x - radius, y - i))  # lower-left
    # for p in points:
    #     assert distance(center, p) == radius
    return points


def get_pos_with_beacons_less_naive(sensors, val_max):
    # Assume we'll be at the (exterior) intersection of at least 3 squares/circles
    sensors_dist = {s: distance(s, b) for s, b in sensors}
    points = dict()
    for s, d in sensors_dist.items():
        for p in get_manhattan_circle(s, d + 1):
            points.setdefault(p, set()).add(s)
    for pos, lst in points.items():
        x, y = pos
        if 0 <= x <= val_max and 0 <= y <= val_max and len(lst) >= 3:
            if all(distance(s, pos) > d for s, d in sensors_dist.items()):
                return get_freq(x, y)


def show_manhattan_square(center=(3, 4), d=5):
    # For debugging purposes (show and check equations)
    i, j = center
    points = {center: "#"}
    sides = get_sides(center, d)
    for x in range(i - d - 1, i + d + 1 + 1):
        for i, (a, b) in enumerate(sides):
            points[(x, a * x + b)] = str(i)
    for (a1, b1), (a2, b2) in itertools.combinations(sides, 2):
        if a1 != a2:
            x = (b2 - b1) / (a1 - a2)
            y = (a1 * b2 - a2 * b1) / (a1 - a2)
            points[(x, y)] = "X"
    xs = [p[0] for p in points.keys()]
    ys = [p[1] for p in points.keys()]
    x_range = list(range(min(xs), max(xs) + 1))
    y_range = list(range(min(ys), max(ys) + 1))
    for x in x_range:
        print("".join(points.get((x, y), " ") for y in y_range))


def get_sides(center, d):
    # Get pairs (a, b) such that sides have equations y = ax + b
    i, j = center
    return [
        (-1, +d + j + i),
        (+1, -d + j - i),
        (+1, +d + j - i),
        (-1, -d + j + i),
    ]


def get_intersections(c1, d1, c2, d2):
    # The boundary of the distance is described by 4 sides whose equations
    # can be written y = ax + b
    # Given 2 such sides defined by y = ax + b and y = cx + d
    #  If a == c, sides are either equal or parallel
    #  Otherwise, single intersection at ((d-b)/(a-c), (ad-bc)/(a-c))
    solutions = []
    for (a1, b1), (a2, b2) in itertools.product(get_sides(c1, d1), get_sides(c2, d2)):
        if a1 == a2:
            pass  # TODO: It could be handled but I'm too lazy
        else:
            x_up, y_up, down = (b2 - b1), (a1 * b2 - a2 * b1), (a1 - a2)
            # Looking for integer solutions
            x_q, x_r = divmod(x_up, down)
            y_q, y_r = divmod(y_up, down)
            if x_r == y_r == 0:
                solutions.append((x_q, y_q))
    return solutions


def get_pos_with_beacons(sensors, val_max):
    # Assume we'll be at the (exterior) intersection of 2 squares/circles
    sensors_dist = {s: distance(s, b) for s, b in sensors}
    boundaries = {s: d + 1 for s, d in sensors_dist.items()}
    for sens1, sens2 in itertools.combinations(boundaries.items(), 2):
        for p in get_intersections(*sens1, *sens2):
            x, y = p
            if 0 <= x <= val_max and 0 <= y <= val_max:
                if all(distance(s, p) > d for s, d in sensors_dist.items()):
                    return get_freq(x, y)


def run_tests():
    sensors = get_sensor_from_lines(
        """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
    )
    assert get_pos_without_beacons(sensors, y_arg=10) == 26
    assert get_manhattan_circle((100, 200), 5) == set(
        [
            (95, 200),
            (96, 199),
            (96, 201),
            (97, 198),
            (97, 202),
            (98, 197),
            (98, 203),
            (99, 196),
            (99, 204),
            (100, 195),
            (100, 205),
            (101, 196),
            (101, 204),
            (102, 197),
            (102, 203),
            (103, 198),
            (103, 202),
            (104, 199),
            (104, 201),
            (105, 200),
        ]
    )
    assert get_pos_with_beacons_naive(sensors, val_max=20) == 56000011
    assert get_pos_with_beacons_less_naive(sensors, val_max=20) == 56000011
    assert get_pos_with_beacons(sensors, val_max=20) == 56000011


def get_solutions():
    sensors = get_sensor_from_file()
    print(get_pos_without_beacons(sensors, y_arg=2000000) == 4811413)
    print(get_pos_with_beacons(sensors, val_max=4000000) == 13171855019123)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
