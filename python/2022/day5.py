# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re

MOVE_RE = re.compile("move (\d+) from (\d+) to (\d+)")

def get_input_from_lines(string):
    lines = string.splitlines()
    # Split stacks and instructions
    empty_idx = lines.index("")
    stacks, instructions = lines[:empty_idx], lines[empty_idx+1:]
    # Parse stacks (transpose then parse)
    parsed_stacks = dict()
    for stack in [i for i in zip(*reversed(stacks))][1::4]:
        # Use tuple to avoid future modifications
        nb, crates = int(stack[0]), tuple(c for c in stack[1:] if c != ' ')
        parsed_stacks[nb] = crates
    parsed_instructions = [tuple(int(g) for g in MOVE_RE.fullmatch(ins).groups())
                           for ins in instructions]
    return parsed_stacks, parsed_instructions


def get_input_from_file(file_path="../../resources/year2022_day5_input.txt"):
    with open(file_path) as f:
        return get_input_from_lines(f.read())


def part1(input_):
    original_stacks, instructions = input_
    stacks = {k: list(v) for k, v in original_stacks.items()}
    for nb, src, dst in instructions:
        stack_src, stack_dst = stacks[src], stacks[dst]
        for _ in range(nb):
            stack_dst.append(stack_src.pop(-1))
    return "".join(stacks[k][-1] for k in sorted(stacks.keys()))

def run_tests():
    input_ = get_input_from_lines("""    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2""")
    assert part1(input_) == "CMZ"

def get_solutions():
    input_ = get_input_from_file()
    print(part1(input_) == "VQZNJMWTR")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
