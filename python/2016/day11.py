# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections
import itertools
import functools
import heapq


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

SKIP_SLOW = True

Component = collections.namedtuple("Component", ("element", "is_generator"))


def get_component_from_string(string):
    string = string.replace("-compatible", "")
    lst = string.split()
    return Component(lst[1], lst[2] == "generator")


def get_floor_from_line(string):
    sep = "contains "
    _, mid, right = string.partition(sep)
    assert mid == sep
    assert right.endswith(".")
    right = right[:-1]
    if right == "nothing relevant":
        return []
    return [
        get_component_from_string(s)
        for s in right.replace(", and", ",").replace(" and", ",").split(", ")
    ]


def get_floors_from_lines(string):
    return tuple(get_floor_from_line(l) for l in string.splitlines())


def get_floors_from_file(file_path=resource_dir + "year2016_day11_input.txt"):
    with open(file_path) as f:
        return get_floors_from_lines(f.read())


def show_floors(floors):
    for i, f in reversed(list(enumerate(floors, start=1))):
        print(i, " ".join(c.element + ("G" if c.is_generator else "M") for c in f))


def checked_set(coll):
    s = set(coll)
    assert len(s) == len(coll)
    return s


def is_floor_valid(floor):
    generators = set(c.element for c in floor if c.is_generator)
    return len(generators) == 0 or all(
        c.element in generators for c in floor - generators
    )


@functools.lru_cache
def get_removable_elements(floor):
    floor = checked_set(floor)
    removed_remaining = []
    removed_remaining_pairs = dict()
    for to_remove in itertools.chain(
        itertools.combinations(floor, 2), itertools.combinations(floor, 1)
    ):
        removed = set(to_remove)
        remaining = floor - removed
        if is_floor_valid(remaining):
            if len(removed) == 2:
                elements = set(c.element for c in removed)
                if len(elements) == 1:
                    removed_remaining_pairs[elements.pop()] = (removed, remaining)
                    continue
            removed_remaining.append((removed, remaining))
    # Any combinations of (generator, chip) for a given element are equivalent - pick the smallest one
    if removed_remaining_pairs:
        smallest = min(removed_remaining_pairs.keys())
        removed_remaining.append(removed_remaining_pairs[smallest])
    return removed_remaining


def collect_to_fourth_floor(floors):
    last_floor = 3
    assert all(is_floor_valid(set(f)) for f in floors)
    nb_comp = sum(len(f) for f in floors)
    initial_state = (
        -len(floors[last_floor]),
        0,
        0,
        tuple(tuple(f) for f in floors),
    )  # -in_place, steps, elevator level, floor content
    heap = [initial_state]
    seen = set()
    while heap:
        in_place, steps, elevator, floors = heapq.heappop(heap)
        in_place = -in_place
        if in_place == nb_comp:
            return steps
        state = (elevator, floors)
        if state in seen:
            continue
        seen.add(state)
        removed_remaining = get_removable_elements(floors[elevator])
        if removed_remaining:
            steps2 = steps + 1
            for direction in (1, -1):
                elevator2 = elevator + direction
                if 0 <= elevator2 <= last_floor:
                    floor2 = checked_set(floors[elevator2])
                    for removed, remaining in removed_remaining:
                        floor3 = floor2 | removed
                        if is_floor_valid(floor3):
                            floors2 = tuple(
                                tuple(floor3)
                                if i == elevator2
                                else (tuple(remaining) if i == elevator else f)
                                for i, f in enumerate(floors)
                            )
                            heapq.heappush(
                                heap,
                                (-len(floors2[last_floor]), steps2, elevator2, floors2),
                            )


def run_tests():
    floors = get_floors_from_lines(
        """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."""
    )
    assert collect_to_fourth_floor(floors) == 11


def get_solutions():
    floors = get_floors_from_file()
    print(collect_to_fourth_floor(floors) == 33)
    new_components = [
        get_component_from_string(s)
        for s in (
            "An elerium generator",
            "An elerium-compatible microchip",
            "A dilithium generator",
            "A dilithium-compatible microchip",
        )
    ]
    floors[0].extend(new_components)
    if not SKIP_SLOW:
        # This takes around 12 minutes at the moment :(
        print(collect_to_fourth_floor(floors) == 57)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
