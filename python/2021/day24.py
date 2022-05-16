# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import math
import itertools


def get_program_from_file(file_path="day24_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def get_val(alu, var_or_number):
    if var_or_number in alu:
        return alu[var_or_number]
    return int(var_or_number)


def truncate_div(a, b):
    q = a / b
    return math.floor(q) if q >= 0 else math.ceil(q)


def run_program(program, input_val):
    alu = {var: 0 for var in "wxyz"}
    for line in program:
        line = line.split(" ")
        instruction = line[0]
        dest = line[1]
        if instruction == "inp":
            inp = next(input_val)
            # assert 1 <= inp <= 9
            alu[dest] = inp
        elif instruction == "add":
            alu[dest] += get_val(alu, line[2])
        elif instruction == "mul":
            alu[dest] *= get_val(alu, line[2])
        elif instruction == "div":
            alu[dest] = truncate_div(alu[dest], get_val(alu, line[2]))
        elif instruction == "mod":
            alu[dest] %= get_val(alu, line[2])
        elif instruction == "eql":
            alu[dest] = int(alu[dest] == get_val(alu, line[2]))
        else:
            assert False
        if 0:
            print(line)
            print(alu)
            input("Enter to continue")
    return alu


def run_tests():
    assert truncate_div(0, 2) == 0
    assert truncate_div(4, 2) == 2
    assert truncate_div(5, 2) == 2
    assert truncate_div(-4, 2) == -2
    assert truncate_div(-5, 2) == -2

    program = [
        "inp z",
        "inp x",
        "mul z 3",
        "eql z x",
    ]
    assert run_program(program, iter([1, 3]))["z"] == 1
    assert run_program(program, iter([2, 6]))["z"] == 1
    assert run_program(program, iter([1, 2]))["z"] == 0
    assert run_program(program, iter([2, 7]))["z"] == 0

    program = [
        "inp w",
        "add z w",
        "mod z 2",
        "div w 2",
        "add y w",
        "mod y 2",
        "div w 2",
        "add x w",
        "mod x 2",
        "div w 2",
        "mod w 2",
    ]
    for i in range(16):
        res = run_program(program, iter([i]))
        i, rem = divmod(i, 2)
        assert res["z"] == rem
        i, rem = divmod(i, 2)
        assert res["y"] == rem
        i, rem = divmod(i, 2)
        assert res["x"] == rem
        i, rem = divmod(i, 2)
        assert res["w"] == rem


def monad_bruteforce(program):
    # This will never work - a better solution is to be found
    maxi = int("9" * 14)
    for i in itertools.count(maxi, -1):
        i_lst = [int(d) for d in str(i)]
        if 0 not in i_lst:
            res = run_program(program, iter(i_lst))
            if res["z"] == 0:
                return i
    assert False


def monad_analysis(program):
    input_positions = [i for i, l in enumerate(program) if l.startswith("inp ")]
    for nb_dig in (1, 2, 3, 4):
        prog = program[: input_positions[nb_dig]]
        for inp in itertools.product(range(1, 10), repeat=nb_dig):
            res = run_program(prog, iter(inp))
            if nb_dig == 1:
                assert res["w"] == inp[-1]
                assert res["x"] == 1
                assert res["y"] == res["z"] == inp[0] + 8
            elif nb_dig == 2:
                assert res["w"] == inp[-1]
                assert res["x"] == 1
                assert res["y"] == inp[1] + 13
                assert res["z"] == inp[1] + 13 + 26 * (inp[0] + 8)
                assert res["z"] == 221 + inp[1] + 26 * inp[0]
            elif nb_dig == 3:
                assert res["w"] == inp[-1]
                assert res["x"] == 1
                assert res["y"] == inp[2] + 8


def get_solutions():
    program = get_program_from_file()
    return monad_analysis(program)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    #     run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
