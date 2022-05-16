# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools
import heapq


def get_points_from_lines(lines):
    moving_parts = dict()
    points = set()
    for i, line in enumerate(lines):
        for j, val in enumerate(line):
            pos = (i, j)
            if val == ".":
                points.add(pos)
            elif val in ("ABCD"):
                points.add(pos)
                moving_parts[pos] = val
    return points, moving_parts


def get_points_from_file(file_path="day23_input.txt"):
    with open(file_path) as f:
        return get_points_from_lines([l.rstrip() for l in f])


def show_points(points, moving_parts):
    points_val = {p: "." for p in points}
    for pos, val in moving_parts.items():
        assert pos in points_val
        points_val[pos] = val
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    x_range = list(range(min(x_vals), 1 + max(x_vals)))
    y_range = list(range(min(y_vals), 1 + max(y_vals)))
    for x in x_range:
        print("".join(points_val.get((x, y), "#") for y in y_range), x)
    print("".join(str(y) for y in y_range))
    print()


def neighbours(p):
    x, y = p
    for delta in (-1, 1):
        yield x + delta, y
        yield x, y + delta


def get_graph(points, moving_parts):
    free_points = points - moving_parts.keys()
    return {p: set(p2 for p2 in neighbours(p) if p2 in free_points) for p in points}


def shortest_paths(graph, start):
    distances = dict()
    queue = [(0, start)]
    while queue:
        d, pos = queue.pop(0)
        if pos in distances:
            assert d >= distances[pos]
        else:
            distances[pos] = d
            if all(p in distances for p in graph):
                break
            for pos2 in graph[pos]:
                if pos2 in distances:
                    assert d + 1 >= distances[pos2]
                else:
                    queue.append((d + 1, pos2))
    return distances


y_vals = {
    "A": 3,
    "B": 5,
    "C": 7,
    "D": 9,
}

energy_vals = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


def destination_rooms(val):
    y = y_vals[val]
    return [(3, y), (2, y)]  # Order matters


def count_wrong_position(moving_parts):
    c = 0
    for val in y_vals:
        for pos in destination_rooms(val):
            if not moving_parts.get(pos, None) == val:
                break
            c += 1
    return len(moving_parts) - c


def get_moves(points, moving_parts):
    graph = get_graph(points, moving_parts)
    # Amphipods will never stop on the space immediately outside any room
    hallway = set((x, y) for x, y in points if x == 1 and y not in (3, 5, 7, 9))
    rooms = set((x, y) for x, y in points if x != 1)
    for pos, val in moving_parts.items():
        destinations = set()
        room_dests = destination_rooms(val)
        assert all(dest in rooms for dest in room_dests)

        # Get final position for element (None if it is busy or if there is no point in going there)
        final_destination = None
        for dest in room_dests:
            if dest == pos:
                # Current position is final position
                final_destination = dest
                break
            val2 = moving_parts.get(dest, None)
            if val2 is None:
                # Free
                final_destination = dest
                break
            elif val2 == val:
                # Busy with correct value - look at next spot
                continue
            else:
                # Busy with incorrect value - stop
                break

        if pos in hallway:
            # Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room
            # Amphipods will never move from the hallway into a room unless that room is their destination room...
            assert pos not in room_dests
            destinations = set([] if final_destination is None else [final_destination])
            assert all(dest in rooms for dest in destinations)
        else:
            # We can try to go almost anywhere
            # But we can be smarter... if it's in the right place: don't move!
            if pos == final_destination:
                destinations = set()
            else:
                destinations = set(room_dests) | hallway

        # Remove origin
        destinations -= set([pos])

        # Generate the moves to the destination
        if destinations:
            energy = energy_vals[val]
            # Compute distances
            distances = shortest_paths(graph, pos)
            for dest in destinations:
                if dest in distances:
                    dist = distances[dest]
                    assert dist > 0
                    # Generate move - copy info and update it
                    cost = dist * energy
                    moving_parts2 = moving_parts.copy()
                    moving_parts2.pop(pos)
                    assert dest not in moving_parts2
                    moving_parts2[dest] = val
                    assert len(moving_parts2) == len(moving_parts)
                    yield cost, moving_parts2


def hash_mp(moving_parts):
    return tuple(sorted(moving_parts.items()))


def organise(points, moving_parts):
    # (nb_wrong_pos, nb_moves, cost, moving_parts)
    heap = [(count_wrong_position(moving_parts), 0, 0, hash_mp(moving_parts))]
    seen = dict()
    solution = None
    while heap:
        nb_wrong_pos, nb_moves, cost, setup = heapq.heappop(heap)
        if setup in seen and cost >= seen[setup]:
            continue
        seen[setup] = cost
        if solution is not None and cost >= solution:
            continue
        setup_dict = dict(setup)
        if nb_wrong_pos == 0:
            solution = cost
            # print(solution, "elements in queue:", len(heap))
            continue
        moves = list(get_moves(points, setup_dict))
        for cost_add, setup2 in moves:
            nb_moves2 = nb_moves + 1
            cost2 = cost + cost_add
            heapq.heappush(
                heap, (count_wrong_position(setup2), nb_moves2, cost2, hash_mp(setup2))
            )
    return solution


def run_tests():
    points1 = [
        "#############",
        "#.........A.#",
        "###.#B#C#D###",
        "  #A#B#C#D#",
        "  #########",
    ]
    energy1 = 8

    points2 = [
        "#############",
        "#.....D.D.A.#",
        "###.#B#C#.###",
        "  #A#B#C#.#",
        "  #########",
    ]
    energy2 = energy1 + 7000

    points4 = [
        "#############",
        "#.....D.....#",
        "###B#.#C#D###",
        "  #A#B#C#A#",
        "  #########",
    ]
    energy4 = energy2 + 2003 + 40

    points5 = [
        "#############",
        "#...B.......#",
        "###B#.#C#D###",
        "  #A#D#C#A#",
        "  #########",
    ]
    energy5 = energy4 + 30 + 3000

    points6 = [
        "#############",
        "#...B.......#",
        "###B#C#.#D###",
        "  #A#D#C#A#",
        "  #########",
    ]
    energy6 = energy5 + 400

    points7 = [
        "#############",
        "#...........#",
        "###B#C#B#D###",
        "  #A#D#C#A#",
        "  #########",
    ]
    energy7 = energy6 + 40

    tests = [
        (points1, energy1),
        (points2, energy2),
        (points4, energy4),
        (points5, energy5),
        (points6, energy6),
        (points7, energy7),
    ]
    for points, energy in tests:
        points, moving_parts = get_points_from_lines(points)
        assert organise(points, moving_parts) == energy


def get_solutions():
    points, moving_parts = get_points_from_file()
    print(organise(points, moving_parts))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
