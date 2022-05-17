# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import string
import collections
import itertools
import heapq


def get_grid_from_file(file_path="../../resources/year2019_day20_input.txt"):
    with open(file_path) as f:
        return [l for l in f]


def points_iter(grid):
    for x, line in enumerate(grid):
        for y, val in enumerate(line):
            yield (x, y), val


def neighbours(pos):
    x, y = pos
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        yield x + dx, y + dy


def get_info(grid):
    passages = set()
    letters = dict()
    for pos, val in points_iter(grid):
        if val == ".":
            passages.add(pos)
        elif val in string.ascii_uppercase:
            letters[pos] = val
        elif val not in " #\n":
            assert False
    return passages, letters


def get_center(grid):
    return (len(grid) // 2, len(grid[0]) // 2)


def get_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def get_labels(letters, passages):
    # Find labels
    labels = dict()
    for pos, val in letters.items():
        neigh = list(neighbours(pos))
        passage = [n for n in neigh if n in passages]
        letter = [n for n in neigh if n in letters]
        if len(letter) == 1 and len(passage) == 1:
            # Sort letters by position top-to-bottom and left-to-right
            letter_pos = sorted([pos, letter[0]])
            label = "".join(letters[p] for p in letter_pos)
            pos2 = passage[0]
            labels.setdefault(label, []).append(pos2)
    # Interpret labels
    entrance = labels.pop("AA")
    exit = labels.pop("ZZ")
    assert len(entrance) == 1
    assert len(exit) == 1
    entrance = entrance[0]
    exit = exit[0]
    return entrance, exit, labels


def print_graph(graph):
    for pos, succs in graph.items():
        print(pos)
        for pos2, d in succs.items():
            print("     ", d, pos2)


def print_distances(points):
    keys = points.keys()
    i_vals = [i for i, _, _ in keys]
    j_vals = [j for _, j, _ in keys]
    k_vals = [k for _, _, k in keys]
    i_range = list(range(min(i_vals), max(i_vals) + 1))
    j_range = list(range(min(j_vals), max(j_vals) + 1))
    k_range = list(range(min(k_vals), max(k_vals) + 1))
    for k in k_range:
        print("Level ", k)
        for i in i_range:
            print(" ".join(str(points.get((i, j, k), "")).center(2) for j in j_range))


def build_graph(passages):
    return {
        pos: {pos2: 1 for pos2 in neighbours(pos) if pos2 in passages}
        for pos in passages
    }


def add_warps(graph, warps):
    for label, positions in warps.items():
        assert len(positions) == 2
        pos1, pos2 = positions
        graph[pos1][pos2] = 1
        graph[pos2][pos1] = 1


def simplify_graph(graph):
    """Optional method to simplify graph by removing dummy points."""
    # print(len(graph), sum(len(succ) for succ in graph.values()))
    change = True
    while change:
        change = False
        for pos, succs in graph.items():
            n = len(succs)
            if n == 2:
                (p1, d1), (p2, d2) = succs.items()
                del graph[pos]
                del graph[p1][pos]
                del graph[p2][pos]
                graph[p1][p2] = d1 + d2
                graph[p2][p1] = d1 + d2
                change = True
                break
    # print(len(graph), sum(len(succ) for succ in graph.values()))
    # print_graph(graph)
    return graph


def shortest_path(graph, entrance, exit):
    distances = dict()
    heap = [(0, entrance)]
    while heap:
        d, pos = heapq.heappop(heap)
        if pos == exit:
            return d
        if pos in distances:
            assert d >= distances[pos]
            continue
        distances[pos] = d
        for pos2, d2 in graph[pos].items():
            if pos2 not in distances:
                heapq.heappush(heap, ((d + d2), pos2))
    assert False


def solve_maze(grid):
    # Extract relevant info from maze
    passages, letters = get_info(grid)
    # Extract positions for interesting places
    entrance, exit, warps = get_labels(letters, passages)
    graph = build_graph(passages)
    add_warps(graph, warps)
    return shortest_path(graph, entrance, exit)


def solve_maze2(grid):
    # Extract relevant info from maze
    passages, letters = get_info(grid)
    center = get_center(grid)
    # Extract positions for interesting places
    entrance, exit, warps = get_labels(letters, passages)
    graph = build_graph(passages)
    graph = simplify_graph(graph)
    # Bring to next dimensions
    nb_levels = 60
    graph2 = dict()
    for z in range(nb_levels):
        # Add passages on all levels
        for (x, y), succs in graph.items():
            graph2[(x, y, z)] = {(x2, y2, z): d for (x2, y2), d in succs.items()}
    for z in range(nb_levels):
        # Add multi-dimensions wraps
        for label, positions in warps.items():
            assert len(positions) == 2
            inner, outter = sorted(positions, key=lambda p: get_dist(p, center))
            (x_in, y_in), (x_out, y_out) = inner, outter
            # Inner goes to outter higher
            graph2[(x_in, y_in, z)][(x_out, y_out, z + 1)] = 1
            # Outter goes to inner lower
            graph2.setdefault((x_out, y_out, z + 1), dict())[(x_in, y_in, z)] = 1
    # Solve
    in1, in2 = entrance
    out1, out2 = exit
    return shortest_path(graph2, (in1, in2, 0), (out1, out2, 0))


def run_tests():
    grid = [
        "         A           ",
        "         A           ",
        "  #######.#########  ",
        "  #######.........#  ",
        "  #######.#######.#  ",
        "  #######.#######.#  ",
        "  #######.#######.#  ",
        "  #####  B    ###.#  ",
        "BC...##  C    ###.#  ",
        "  ##.##       ###.#  ",
        "  ##...DE  F  ###.#  ",
        "  #####    G  ###.#  ",
        "  #########.#####.#  ",
        "DE..#######...###.#  ",
        "  #.#########.###.#  ",
        "FG..#########.....#  ",
        "  ###########.#####  ",
        "             Z       ",
        "             Z       ",
    ]
    assert solve_maze(grid) == 23
    assert solve_maze2(grid) == 26
    grid = [
        "                   A               ",
        "                   A               ",
        "  #################.#############  ",
        "  #.#...#...................#.#.#  ",
        "  #.#.#.###.###.###.#########.#.#  ",
        "  #.#.#.......#...#.....#.#.#...#  ",
        "  #.#########.###.#####.#.#.###.#  ",
        "  #.............#.#.....#.......#  ",
        "  ###.###########.###.#####.#.#.#  ",
        "  #.....#        A   C    #.#.#.#  ",
        "  #######        S   P    #####.#  ",
        "  #.#...#                 #......VT",
        "  #.#.#.#                 #.#####  ",
        "  #...#.#               YN....#.#  ",
        "  #.###.#                 #####.#  ",
        "DI....#.#                 #.....#  ",
        "  #####.#                 #.###.#  ",
        "ZZ......#               QG....#..AS",
        "  ###.###                 #######  ",
        "JO..#.#.#                 #.....#  ",
        "  #.#.#.#                 ###.#.#  ",
        "  #...#..DI             BU....#..LF",
        "  #####.#                 #.#####  ",
        "YN......#               VT..#....QG",
        "  #.###.#                 #.###.#  ",
        "  #.#...#                 #.....#  ",
        "  ###.###    J L     J    #.#.###  ",
        "  #.....#    O F     P    #.#...#  ",
        "  #.###.#####.#.#####.#####.###.#  ",
        "  #...#.#.#...#.....#.....#.#...#  ",
        "  #.#####.###.###.#.#.#########.#  ",
        "  #...#.#.....#...#.#.#.#.....#.#  ",
        "  #.###.#####.###.###.#.#.#######  ",
        "  #.#.........#...#.............#  ",
        "  #########.###.###.#############  ",
        "           B   J   C               ",
        "           U   P   P               ",
    ]
    assert solve_maze(grid) == 58
    grid = [
        "             Z L X W       C                 ",
        "             Z P Q B       K                 ",
        "  ###########.#.#.#.#######.###############  ",
        "  #...#.......#.#.......#.#.......#.#.#...#  ",
        "  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  ",
        "  #.#...#.#.#...#.#.#...#...#...#.#.......#  ",
        "  #.###.#######.###.###.#.###.###.#.#######  ",
        "  #...#.......#.#...#...#.............#...#  ",
        "  #.#########.#######.#.#######.#######.###  ",
        "  #...#.#    F       R I       Z    #.#.#.#  ",
        "  #.###.#    D       E C       H    #.#.#.#  ",
        "  #.#...#                           #...#.#  ",
        "  #.###.#                           #.###.#  ",
        "  #.#....OA                       WB..#.#..ZH",
        "  #.###.#                           #.#.#.#  ",
        "CJ......#                           #.....#  ",
        "  #######                           #######  ",
        "  #.#....CK                         #......IC",
        "  #.###.#                           #.###.#  ",
        "  #.....#                           #...#.#  ",
        "  ###.###                           #.#.#.#  ",
        "XF....#.#                         RF..#.#.#  ",
        "  #####.#                           #######  ",
        "  #......CJ                       NM..#...#  ",
        "  ###.#.#                           #.###.#  ",
        "RE....#.#                           #......RF",
        "  ###.###        X   X       L      #.#.#.#  ",
        "  #.....#        F   Q       P      #.#.#.#  ",
        "  ###.###########.###.#######.#########.###  ",
        "  #.....#...#.....#.......#...#.....#.#...#  ",
        "  #####.#.###.#######.#######.###.###.#.#.#  ",
        "  #.......#.......#.#.#.#.#...#...#...#.#.#  ",
        "  #####.###.#####.#.#.#.#.###.###.#.###.###  ",
        "  #.......#.....#.#...#...............#...#  ",
        "  #############.#.#.###.###################  ",
        "               A O F   N                     ",
        "               A A D   M                     ",
    ]
    assert solve_maze2(grid) == 396


def get_solutions():
    grid = get_grid_from_file()
    print(solve_maze(grid))
    print(solve_maze2(grid))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
