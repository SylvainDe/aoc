# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import heapq
import collections

Valve = collections.namedtuple("Valve", ["id", "flow", "tunnels"])

# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
valve_re = re.compile(r"^Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)$")

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


def release_pressure(valves, start_time=30, start_pos="AA"):
    sorted_valves = sorted((v.flow, v.id) for v in valves)
    valves = { v.id: v for v in valves }
    heap = [(0, -start_time, tuple(), start_pos)] # (-pressure, time, open, path, pos)
    max_pressure = 0
    while heap:
        n_pressure, n_time, open_, pos = heapq.heappop(heap)
        pressure = -n_pressure
        time = -n_time
        valve = valves[pos]
        if time <= 0:
            continue
        open_set = set(open_)
        rem_time = time - 1
        if pressure > max_pressure:
            max_pressure = pressure
        still_closed = [f for f, id_ in sorted_valves if id_ not in open_set]
        max_reachable = sum(t * f for t, f in zip(reversed(range(rem_time%2, rem_time+1, 2)), reversed(still_closed)))
        if pressure + max_reachable < max_pressure:
            continue
        # Open at current position
        if valve.id not in open_set and valve.flow:
            open_set.add(valve.id)
            heapq.heappush(heap, (
                -(pressure + valve.flow * rem_time),
                -rem_time,
                tuple(sorted(open_set)),
                pos))
        # Go through tunnel
        for d in valve.tunnels:
            heapq.heappush(heap, (
                n_pressure,
                -rem_time,
                open_,
                d))
    return max_pressure




def run_tests():
    valves = get_valves_from_lines("""Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""")
    assert release_pressure(valves) == 1651

def get_solutions():
    valves = get_valves_from_file()
    # print(release_pressure(valves)) - super slow :(


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
