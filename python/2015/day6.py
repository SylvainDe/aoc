# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools
import collections

verbs = ["turn on", "toggle", "turn off"]


def get_point_from_string(s, sep=","):
    left, mid, right = s.partition(sep)
    assert mid == sep
    return int(left), int(right)


def get_range_from_string(s, sep=" through "):
    left, mid, right = s.partition(sep)
    assert mid == sep
    return get_point_from_string(left), get_point_from_string(right)


def get_instruction_from_string(s):
    for verb in verbs:
        if s.startswith(verb):
            return verb, get_range_from_string(s[len(verb) + 1 :])
    assert False


def get_instructions_from_file(file_path="day6_input.txt"):
    with open(file_path) as f:
        return [get_instruction_from_string(l.strip()) for l in f]


def get_points(points):
    (x1, y1), (x2, y2) = points
    min_x, max_x = sorted([x1, x2])
    min_y, max_y = sorted([y1, y2])
    return itertools.product(range(min_x, max_x + 1), range(min_y, max_y + 1))


def apply_instruction(lights, instruction):
    verb, points = instruction
    for p in get_points(points):
        add = None
        if verb == "turn on":
            add = True
        elif verb == "turn off":
            add = False
        elif verb == "toggle":
            add = p not in lights
        assert add is not None
        if add:
            lights.add(p)
        else:
            lights.discard(p)


def apply_instructions(instructions):
    lights = set()
    for ins in instructions:
        apply_instruction(lights, ins)
    return lights


def apply_instruction2(lights, instruction):
    verb, points = instruction
    for p in get_points(points):
        if verb == "turn on":
            lights[p] += 1
        elif verb == "turn off":
            lights[p] = max(lights[p] - 1, 0)
        elif verb == "toggle":
            lights[p] += 2
        else:
            assert False


def apply_instructions2(instructions):
    lights = collections.defaultdict(int)
    for ins in instructions:
        apply_instruction2(lights, ins)
    return lights


def run_tests():
    assert len(list(get_points(get_range_from_string("0,0 through 999,0")))) == 1000
    assert len(list(get_points(get_range_from_string("499,499 through 500,500")))) == 4


def get_solutions():
    instructions = get_instructions_from_file()
    print(len(apply_instructions(instructions)))
    print(sum(apply_instructions2(instructions).values()))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
