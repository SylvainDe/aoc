# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

MOVE_RE = re.compile(r"move (\d+) from (\d+) to (\d+)")


def get_input_from_lines(string):
    lines = string.splitlines()
    # Split stacks and instructions
    empty_idx = lines.index("")
    stacks, instructions = lines[:empty_idx], lines[empty_idx + 1 :]
    # Parse stacks (transpose then parse)
    parsed_stacks = {}
    for stack in list(zip(*reversed(stacks)))[1::4]:
        # Use tuple to avoid future modifications
        nb, crates = int(stack[0]), tuple(c for c in stack[1:] if c != " ")
        parsed_stacks[nb] = crates
    parsed_instructions = [
        tuple(int(g) for g in MOVE_RE.fullmatch(ins).groups()) for ins in instructions
    ]
    return parsed_stacks, parsed_instructions


def get_input_from_file(file_path=resource_dir + "year2022_day5_input.txt"):
    with open(file_path) as f:
        return get_input_from_lines(f.read())


def do_crane_operations(input_, is_fifo):
    original_stacks, instructions = input_
    stacks = {k: list(v) for k, v in original_stacks.items()}
    for nb, src, dst in instructions:
        stack_src, stack_dst = stacks[src], stacks[dst]
        popped = [stack_src.pop(-1) for _ in range(nb)]
        stack_dst.extend(popped if is_fifo else reversed(popped))
    return "".join(stacks[k][-1] for k in sorted(stacks.keys()))


def part1(input_):
    return do_crane_operations(input_, is_fifo=True)


def part2(input_):
    return do_crane_operations(input_, is_fifo=False)


def run_tests():
    input_ = get_input_from_lines(
        """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
    )
    assert part1(input_) == "CMZ"
    assert part2(input_) == "MCD"


def get_solutions():
    input_ = get_input_from_file()
    print(part1(input_) == "VQZNJMWTR")
    print(part2(input_) == "NLCDCLVMQ")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
