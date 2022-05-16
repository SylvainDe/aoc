# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_wires_from_file(file_path="day3_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


directions = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}


def get_wire_path(wire):
    x, y = 0, 0
    for instruction in wire.split(","):
        (dx, dy), value = directions[instruction[0]], int(instruction[1:])
        for i in range(value):
            x += dx
            y += dy
            yield x, y


def get_crossing_min_distance(wires):
    crossings = set.intersection(*(set(get_wire_path(w)) for w in wires))
    distances = [abs(x) + abs(y) for x, y in crossings]
    return min(distances)


def get_crossing_min_delay(wires):
    paths = dict()
    for w in wires:
        first_visit = dict()
        for step, pos in enumerate(get_wire_path(w)):
            if pos not in first_visit:
                first_visit[pos] = step
        for pos, step in first_visit.items():
            paths.setdefault(pos, []).append(step)
    crossings = [steps for steps in paths.values() if len(steps) == 2]
    steps = [sum(steps) + 2 for steps in crossings]
    return min(steps)


def run_tests():
    wires = ["R8,U5,L5,D3", "U7,R6,D4,L4"]
    assert get_crossing_min_distance(wires) == 6
    assert get_crossing_min_delay(wires) == 30
    wires = ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]
    assert get_crossing_min_distance(wires) == 159
    assert get_crossing_min_delay(wires) == 610


def get_solutions():
    wires = get_wires_from_file()
    print(get_crossing_min_distance(wires))
    print(get_crossing_min_delay(wires))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
