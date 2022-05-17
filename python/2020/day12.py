# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
from enum import Enum


def get_instructions_from_file(file_path="../../resources/year2020_day12_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


#      y ^ NORTH
#        |
# WEST   |       EAST
# -------+-----> x
#        |
#        |
#        | SOUTH

shifting = {
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
    "N": (0, 1),
}

rotations = ["E", "S", "W", "N"]


def state_after_instruction(state, instruction):
    x, y, direc = state
    action, n = instruction[0], int(instruction[1:])
    if action in shifting:
        dx, dy = shifting[action]
        x, y = x + n * dx, y + n * dy
    elif action == "F":
        dx, dy = shifting[direc]
        x, y = x + n * dx, y + n * dy
    elif action in ("L", "R"):
        rot = (-1 if action == "L" else 1) * n // 90
        direc = rotations[(rotations.index(direc) + rot) % 4]
    else:
        1 / 0
    return x, y, direc


def state_after_instructions(instructions):
    state = (0, 0, "E")
    for ins in instructions:
        state = state_after_instruction(state, ins)
    return state


def state_after_instruction2(state, instruction):
    xs, ys, xw, yw = state
    action, n = instruction[0], int(instruction[1:])
    if action in shifting:
        dx, dy = shifting[action]
        xw, yw = xw + n * dx, yw + n * dy
    elif action == "F":
        xs, ys = xs + n * xw, ys + n * yw
    elif action in ("L", "R"):
        rot = ((-1 if action == "L" else 1) * n // 90) % 4
        for i in range(rot):
            xw, yw = yw, -xw
    else:
        1 / 0
    return xs, ys, xw, yw


def state_after_instructions2(instructions):
    state = (0, 0, 10, 1)
    for ins in instructions:
        state = state_after_instruction2(state, ins)
    return state


def run_tests():
    example1 = [
        "F10",
        "N3",
        "F7",
        "R90",
        "F11",
    ]
    x, y, direct = state_after_instructions(example1)
    assert abs(x) + abs(y) == 25
    x, y, xw, yw = state_after_instructions2(example1)
    assert abs(x) + abs(y) == 286


def get_solutions():
    instructions = get_instructions_from_file()
    x, y, direct = state_after_instructions(instructions)
    print(abs(x) + abs(y) == 381)
    x, y, xw, yw = state_after_instructions2(instructions)
    print(abs(x) + abs(y) == 28591)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
