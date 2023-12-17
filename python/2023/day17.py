# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import heapq


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_grid_from_lines(string):
    grid = dict()
    for i, row in enumerate(string.splitlines()):
        for j, cell in enumerate(row):
            grid[(i, j)] = int(cell)
    return grid


def get_grid_from_file(file_path=top_dir + "resources/year2023_day17_input.txt"):
    with open(file_path) as f:
        return get_grid_from_lines(f.read())

directions = [(-1, 0), (+1, 0), (0, -1), (0, +1)]


def manhattan_dist(p1, p2):
    return sum(abs(c2 - c1) for c1, c2 in zip(p1, p2))

def show_path(path):
    grid = dict()
    for i, pos in enumerate(path):
        grid.setdefault(pos, []).append(i)
    xs = [p[0] for p in grid]
    ys = [p[1] for p in grid]
    for x in range(min(xs), max(xs)+1):
        for y in range(min(ys), max(ys)+1):
            pos = x, y
            print(grid[pos][0] % 10 if pos in grid else " ", end="")
        print()
    print()


def get_minimal_heat(grid):
    starting_pos, end_pos = (0, 0), (max(x for x, _ in grid), (max(y for _, y in grid)))
    nb_max_consec_move = 3
    # (heat, nb_consec_move, last_move, position)
    heap = [(0, 0, None, starting_pos, [])]
    seen = dict()
    while heap:
        heat, nb_consec_move, last_move, position, path = heapq.heappop(heap)
        if position == end_pos:
            # cum_heat = 0
            # for i, pos in enumerate(path):
            #     heat = grid[pos]
            #     cum_heat += heat
            #     print(i, pos, heat, cum_heat)
            return heat
        state = (nb_consec_move, last_move, position)
        seen_heat = seen.get(state)
        if seen_heat is not None and seen_heat <= heat:
            continue
        seen[state] = heat
        i, j = position
        for direct in directions:
            di, dj = direct
            if last_move == (-di, -dj):
                continue
            nb_consec_move2 = 1 + (nb_consec_move if direct == last_move else 0)
            if nb_consec_move2 > nb_max_consec_move:
                continue
            pos2 = (i+di, j+dj)
            heat_val = grid.get(pos2, None)
            if heat_val is not None:
                state2 = (heat+heat_val, nb_consec_move2, direct, pos2, path + [pos2])
                heapq.heappush(heap, state2)
    assert False


def run_tests():
    grid = get_grid_from_lines(
        """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
    )
    assert get_minimal_heat(grid) == 102


def get_solutions():
    grid = get_grid_from_file()
    print(get_minimal_heat(grid) == 1260)

if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
