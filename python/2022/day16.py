# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import heapq
import collections

Valve = collections.namedtuple("Valve", ["id", "flow", "tunnels"])

# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
valve_re = re.compile(
    r"^Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)$"
)


def get_valves_from_line(string):
    id_, flow, tunnels = valve_re.match(string).groups()
    flow = int(flow)
    tunnels = tuple(tunnels.split(", "))
    return Valve(id_, flow, tunnels)


def get_valves_from_lines(string):
    return [get_valves_from_line(l) for l in string.splitlines()]


def get_valves_from_file(file_path="../../resources/year2022_day16_input.txt"):
    with open(file_path) as f:
        return get_valves_from_lines(f.read())


def floyd_marshall(valves):
    graph = {v.id: v.tunnels for v in valves}
    distances = dict()
    for src, dsts in graph.items():
        for dst in dsts:
            distances[(src, dst)] = 1
    for k in graph.keys():
        for i in graph.keys():
            for j in graph.keys():
                d1 = distances.get((i, k), None)
                d2 = distances.get((k, j), None)
                if d1 is not None and d2 is not None:
                    d3 = d1 + d2
                    d = min(distances.get((i, j), d3), d3)
                    distances[(i, j)] = d
    return distances


def floyd_marshall_clean(valves, start_pos):
    distances = floyd_marshall(valves)
    relevant = set(v.id for v in valves if v.flow > 0)
    clean_distances = {(start_pos, start_pos): 0}
    for (i, j), d in floyd_marshall(valves).items():
        if (i in relevant or i == start_pos) and j in relevant:
            clean_distances.setdefault(i, []).append((j, d))
    return clean_distances


def release_pressure(valves, start_time=30, start_pos="AA"):
    distances = floyd_marshall_clean(valves, start_pos)
    sorted_valves = sorted(((v.flow, v.id) for v in valves if v.flow), reverse=True)
    valves = {v.id: v for v in valves}
    heap = [(0, -start_time, tuple(), start_pos)]  # (-pressure, -time, open, pos)
    max_pressure = 0
    while heap:
        n_pressure, n_time, open_, pos = heapq.heappop(heap)
        pressure = -n_pressure
        time = -n_time
        if time <= 0:
            continue
        open_set = set(open_)
        if pressure > max_pressure:
            max_pressure = pressure
        still_closed = (f for f, id_ in sorted_valves if id_ not in open_set)
        rem_time = time - 1
        usable_times = list(reversed(range(rem_time + 1)))[::2]
        max_reachable = sum(t * f for t, f in zip(usable_times, still_closed))
        if pressure + max_reachable <= max_pressure:
            continue
        # Go through tunnel and open
        for new_pos, d in distances[pos]:
            if new_pos not in open_set:
                new_valve = valves[new_pos]
                time_after_activation = time - d - 1
                pressure_after_activation = (
                    pressure + new_valve.flow * time_after_activation
                )
                heapq.heappush(
                    heap,
                    (
                        -pressure_after_activation,
                        -time_after_activation,
                        tuple(set(list(open_) + [new_pos])),
                        new_pos,
                    ),
                )
    return max_pressure


def release_pressure_with_elephant(valves, start_time=26, start_pos="AA"):
    distances = floyd_marshall_clean(valves, start_pos)
    sorted_valves = sorted(((v.flow, v.id) for v in valves if v.flow), reverse=True)
    valves = {v.id: v for v in valves}
    heap = [
        (0, -start_time, -start_time, tuple(), start_pos, start_pos)
    ]  # (-pressure, -time, -time, open, pos, pos)
    max_pressure = 0
    while heap:
        n_pressure, n_time, n_time2, open_, pos, pos2 = heapq.heappop(heap)
        pressure = -n_pressure
        time, time2 = -n_time, -n_time2
        # Inverse to take entity with most time
        if time2 > time:
            time, time2 = time2, time
            pos, pos2, = (
                pos2,
                pos,
            )
        assert time >= time2
        if time <= 0:
            continue
        open_set = set(open_)
        rem_time = time - 1
        if pressure > max_pressure:
            max_pressure = pressure
        still_closed = [f for f, id_ in sorted_valves if id_ not in open_set]
        usable_times1 = list(reversed(range(rem_time + 1)))[::2]
        usable_times2 = list(reversed(range(time2)))[::2]
        usable_times = sorted(list(usable_times1) + list(usable_times2), reverse=True)
        max_reachable = sum(t * f for t, f in zip(usable_times, still_closed))
        if pressure + max_reachable <= max_pressure:
            continue
        # Go through tunnel and open
        for new_pos, d in distances[pos]:
            if new_pos not in open_set:
                new_valve = valves[new_pos]
                time_after_activation = time - d - 1
                pressure_after_activation = (
                    pressure + new_valve.flow * time_after_activation
                )
                heapq.heappush(
                    heap,
                    (
                        -pressure_after_activation,
                        -time_after_activation,
                        -time2,
                        tuple(set(list(open_) + [new_pos])),
                        new_pos,
                        pos2,
                    ),
                )
    return max_pressure


def run_tests():
    valves = get_valves_from_lines(
        """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
    )
    assert release_pressure(valves) == 1651
    assert release_pressure_with_elephant(valves) == 1707


def get_solutions():
    valves = get_valves_from_file()
    print(release_pressure(valves) == 1737)
    print(release_pressure_with_elephant(valves) == 2216)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
