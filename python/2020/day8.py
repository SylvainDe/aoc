# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_program_from_file(file_path=top_dir + "resources/year2020_day8_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def get_instruction(string):
    op, arg = string.split()
    return op, int(arg)


def get_state_after(program, pos, acc):
    op, arg = get_instruction(program[pos])
    if op == "nop":
        return pos + 1, acc
    elif op == "jmp":
        return pos + arg, acc
    elif op == "acc":
        return pos + 1, acc + arg
    raise ValueError("Invalid op:", op)


def run_program_until_loop(program):
    """Return tuple (loop, acc) where loop is True if loop is found else False."""
    pos, acc = 0, 0
    visited = set([pos])
    while True:
        try:
            pos, acc = get_state_after(program, pos, acc)
        except IndexError:
            return False, acc
        if pos in visited:
            return True, acc
        visited.add(pos)


def fix_program(program):
    for i, line in enumerate(program):
        op, arg = get_instruction(line)
        if op == "nop":
            new_op = "jmp"
        elif op == "jmp":
            new_op = "nop"
        else:
            continue
        new_program = list(program)
        new_program[i] = new_op + " " + str(arg)
        try:
            loop, acc = run_program_until_loop(new_program)
            if not loop:
                return acc
        except IndexError:
            pass
    return None


def run_tests():
    example1 = [
        "nop +0",
        "acc +1",
        "jmp +4",
        "acc +3",
        "jmp -3",
        "acc -99",
        "acc +1",
        "jmp -4",
        "acc +6",
    ]
    example2 = [
        "nop +0",
        "acc +1",
        "jmp +4",
        "acc +3",
        "jmp -3",
        "acc -99",
        "acc +1",
        "nop -4",
        "acc +6",
    ]

    assert run_program_until_loop(example1) == (True, 5)
    assert run_program_until_loop(example2) == (False, 8)
    assert fix_program(example1) == 8


def get_solutions():
    program = get_program_from_file()
    print(run_program_until_loop(program) == (True, 1521))
    print(fix_program(program) == 1016)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
