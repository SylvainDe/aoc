# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_instructions_from_file(file_path="../../resources/year2016_day2_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def dict_from_grid(grid):
    return {
        (i, j): val
        for i, line in enumerate(grid)
        for j, val in enumerate(line)
        if val != " "
    }


directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "R": (0, 1),
    "L": (0, -1),
}


def get_neighbours(point):
    x, y = point
    return {l: (x + dx, y + dy) for l, (dx, dy) in directions.items()}


def get_graph_from_points(points):
    graph = dict()
    for p in points:
        graph[p] = {l: p2 for l, p2 in get_neighbours(p).items() if p2 in points}
    return graph


def follow_instruction(graph, instruction, start):
    p = start
    for ins in instruction:
        p = graph[p].get(ins, p)
    return p


def follow_instructions(grid, instructions, start):
    p = start
    points = dict_from_grid(grid)
    graph = get_graph_from_points(points)
    ret = []
    for ins in instructions:
        p = follow_instruction(graph, ins, p)
        ret.append(points[p])
    return "".join(ret)


keypad = ["123", "456", "789"]
start = (1, 1)
keypad2 = [
    "  1",
    " 234",
    "56789",
    " ABC",
    "  D",
]
start2 = (2, 0)


def run_tests():
    instructions = [
        "ULL",
        "RRDDD",
        "LURDL",
        "UUUUD",
    ]
    assert follow_instructions(keypad, instructions, start) == "1985"
    assert follow_instructions(keypad2, instructions, start2) == "5DB3"


def get_solutions():
    instructions = get_instructions_from_file()
    print(follow_instructions(keypad, instructions, start) == "53255")
    print(follow_instructions(keypad2, instructions, start2) == "7423A")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
