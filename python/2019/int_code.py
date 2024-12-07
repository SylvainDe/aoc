# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import collections
import itertools
import collections


def get_intcode_from_string(s):
    return [int(v) for v in s.split(",")]


def get_intcode_from_file(file_path):
    with open(file_path) as f:
        for l in f:
            return get_intcode_from_string(l)


def parse_op_code(op):
    """Return op, mode1, mode2, mode3."""
    p100, de = divmod(op, 100)
    p1000, c = divmod(p100, 10)
    p10000, b = divmod(p1000, 10)
    _, a = divmod(p10000, 10)
    assert op == a * 10000 + b * 1000 + c * 100 + de
    return de, c, b, a


def get_value(intcode, pos, mode, relative_base):
    val = intcode[pos]
    if mode == 0:  # Position mode
        return intcode[val]
    if mode == 1:  # Immediate mode
        return val
    if mode == 2:  # Relative mode
        return intcode[val + relative_base]
    assert False


def set_value(intcode, pos, mode, relative_base, value):
    val = intcode[pos]
    if mode == 0:  # Position mode
        intcode[val] = value
    elif mode == 2:  # Relative mode
        intcode[val + relative_base] = value
    else:
        assert False


def get_values_from_pos(intcode, pos, modes, relative_base):
    return [
        get_value(intcode, pos + i, mode, relative_base)
        for i, mode in enumerate(modes, start=1)
    ]


RunOutput = collections.namedtuple("RunOutput", ["intcode", "output", "position"])


def run(intcode, input_=[]):
    intcode = collections.defaultdict(int, enumerate(intcode))
    output = []
    input_ = iter(input_)
    pos, relative_base = 0, 0
    while True:
        op, mode1, mode2, mode3 = parse_op_code(intcode[pos])
        # Day 2: opcode 1, 2 and 99
        if op == 99:
            final_intcode = [intcode[v] for v in range(max(intcode) + 1)]
            return RunOutput(final_intcode, output, pos)
        elif op == 1:  # Addition
            a, b = get_values_from_pos(intcode, pos, [mode1, mode2], relative_base)
            set_value(intcode, pos + 3, mode3, relative_base, a + b)
            pos += 4
        elif op == 2:  # Multiplication
            a, b = get_values_from_pos(intcode, pos, [mode1, mode2], relative_base)
            set_value(intcode, pos + 3, mode3, relative_base, a * b)
            pos += 4
        # Day 5 part 1: opcode 3 and 4
        elif op == 3:  # Save-input
            next_input = next(input_)
            assert isinstance(next_input, int)
            set_value(intcode, pos + 1, mode1, relative_base, next_input)
            pos += 2
        elif op == 4:  # Output
            a = get_value(intcode, pos + 1, mode1, relative_base)
            output.append(a)
            pos += 2
        # Day 5 part 2: opcode 5, 6, 7 and 8
        elif op == 5:  # Jump-if-true
            a, b = get_values_from_pos(intcode, pos, [mode1, mode2], relative_base)
            pos = b if a else pos + 3
        elif op == 6:  # Jump-if-false
            a, b = get_values_from_pos(intcode, pos, [mode1, mode2], relative_base)
            pos = b if not a else pos + 3
        elif op == 7:  # Less-then
            a, b = get_values_from_pos(intcode, pos, [mode1, mode2], relative_base)
            set_value(intcode, pos + 3, mode3, relative_base, 1 if a < b else 0)
            pos += 4
        elif op == 8:  # Equals
            a, b = get_values_from_pos(intcode, pos, [mode1, mode2], relative_base)
            set_value(intcode, pos + 3, mode3, relative_base, 1 if a == b else 0)
            pos += 4
        # Day 9: opcode 9
        elif op == 9:  # Relative base
            a = get_value(intcode, pos + 1, mode1, relative_base)
            relative_base += a
            pos += 2
        else:
            assert False


def run_verb_noun(intcode, noun, verb):
    """Specific to day 2 ?."""
    intcode = list(intcode)
    intcode[1] = noun
    intcode[2] = verb
    return run(intcode).intcode[0]


def run_diagnostic(intcode, input_):
    """Specific to day 5 ?."""
    diag = [v for v in run(intcode, [input_]).output if v != 0]
    assert len(diag) == 1
    return diag[0]


def run_circuit(intcode, nbs):
    prev_output = 0
    for nb in nbs:
        prev_output = run(intcode, [nb, prev_output]).output[0]
    return prev_output


def run_circuit_with_feedback(intcode, nbs):
    return 0


def get_circuit_max_output(intcode):
    return max(run_circuit(intcode, p) for p in itertools.permutations(range(4 + 1)))


def run_tests_day2():
    intcode = get_intcode_from_string("1,9,10,3,2,3,11,0,99,30,40,50")
    assert run(intcode) == ([3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50], [], 8)
    assert run_verb_noun(intcode, 9, 10) == 3500
    intcode = get_intcode_from_string("1,0,0,0,99")
    assert run(intcode) == ([2, 0, 0, 0, 99], [], 4)
    assert run_verb_noun(intcode, 0, 0) == 2
    intcode = get_intcode_from_string("2,3,0,3,99")
    assert run(intcode) == ([2, 3, 0, 6, 99], [], 4)
    intcode = get_intcode_from_string("2,4,4,5,99,0")
    assert run(intcode) == ([2, 4, 4, 5, 99, 9801], [], 4)
    intcode = get_intcode_from_string("1,1,1,4,99,5,6,0,99")
    assert run(intcode) == ([30, 1, 1, 4, 2, 5, 6, 0, 99], [], 8)


def run_tests_day5():
    intcode = get_intcode_from_string("3,0,4,0,99")
    for v in range(10):
        assert run(intcode, [v])[1] == [v]
    intcode = get_intcode_from_string("1002,4,3,4,33")
    assert run(intcode) == ([1002, 4, 3, 4, 99], [], 4)
    intcode = get_intcode_from_string("1101,100,-1,4,0")
    assert run(intcode) == ([1101, 100, -1, 4, 99], [], 4)
    intcode = get_intcode_from_string("3,9,8,9,10,9,4,9,99,-1,8")
    assert run(intcode, [8]) == ([3, 9, 8, 9, 10, 9, 4, 9, 99, 1, 8], [1], 8)
    assert run(intcode, [7]) == ([3, 9, 8, 9, 10, 9, 4, 9, 99, 0, 8], [0], 8)
    intcode = get_intcode_from_string("3,9,7,9,10,9,4,9,99,-1,8")
    assert run(intcode, [8]) == ([3, 9, 7, 9, 10, 9, 4, 9, 99, 0, 8], [0], 8)
    assert run(intcode, [7]) == ([3, 9, 7, 9, 10, 9, 4, 9, 99, 1, 8], [1], 8)
    intcode = get_intcode_from_string("3,3,1108,-1,8,3,4,3,99")
    assert run(intcode, [8]) == ([3, 3, 1108, 1, 8, 3, 4, 3, 99], [1], 8)
    assert run(intcode, [7]) == ([3, 3, 1108, 0, 8, 3, 4, 3, 99], [0], 8)
    intcode = get_intcode_from_string("3,3,1107,-1,8,3,4,3,99")
    assert run(intcode, [8]) == ([3, 3, 1107, 0, 8, 3, 4, 3, 99], [0], 8)
    assert run(intcode, [7]) == ([3, 3, 1107, 1, 8, 3, 4, 3, 99], [1], 8)
    intcode = get_intcode_from_string("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
    assert run(intcode, [0]) == (
        [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, 0, 0, 1, 9],
        [0],
        11,
    )
    assert run(intcode, [1]) == (
        [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, 1, 1, 1, 9],
        [1],
        11,
    )
    intcode = get_intcode_from_string("3,3,1105,-1,9,1101,0,0,12,4,12,99,1")
    assert run(intcode, [0]) == (
        [3, 3, 1105, 0, 9, 1101, 0, 0, 12, 4, 12, 99, 0],
        [0],
        11,
    )
    assert run(intcode, [1]) == (
        [3, 3, 1105, 1, 9, 1101, 0, 0, 12, 4, 12, 99, 1],
        [1],
        11,
    )
    intcode = get_intcode_from_string(
        "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
    )
    assert run(intcode, [7]).output == [999]
    assert run(intcode, [8]).output == [1000]
    assert run(intcode, [9]).output == [1001]


def run_tests_day7_part1():
    intcode = get_intcode_from_string("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0")
    assert run_circuit(intcode, [4, 3, 2, 1, 0]) == 43210
    assert get_circuit_max_output(intcode) == 43210

    intcode = get_intcode_from_string(
        "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
    )
    assert run_circuit(intcode, [0, 1, 2, 3, 4]) == 54321
    assert get_circuit_max_output(intcode) == 54321

    intcode = get_intcode_from_string(
        "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
    )
    assert run_circuit(intcode, [1, 0, 4, 3, 2]) == 65210
    assert get_circuit_max_output(intcode) == 65210


def run_tests_day7_part2():
    intcode = get_intcode_from_string(
        "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
    )
    run_circuit_with_feedback(intcode, [9, 8, 7, 6, 5])

    intcode = get_intcode_from_string(
        "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
    )
    run_circuit_with_feedback(intcode, [9, 8, 7, 6, 5])


def run_tests_day7():
    run_tests_day7_part1()
    run_tests_day7_part2()


def run_tests_day9():
    intcode = get_intcode_from_string(
        "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    )
    assert run(intcode).output == intcode
    intcode = get_intcode_from_string("1102,34915192,34915192,7,4,7,99,0")
    assert run(intcode).output == [1219070632396864]
    intcode = get_intcode_from_string("104,1125899906842624,99")
    assert run(intcode).output == [1125899906842624]
    # More tests from Reddit: https://www.reddit.com/r/adventofcode/comments/e8aw9j/comment/fac3294/?utm_source=share&utm_medium=web2x&context=3
    intcode = get_intcode_from_string("109,-1,4,1,99")
    assert run(intcode).output == [-1]
    intcode = get_intcode_from_string("109,-1,104,1,99")
    assert run(intcode).output == [1]
    intcode = get_intcode_from_string("109,-1,204,1,99")
    assert run(intcode).output == [109]
    intcode = get_intcode_from_string("109,1,9,2,204,-6,99")
    assert run(intcode).output == [204]
    intcode = get_intcode_from_string("109,1,109,9,204,-6,99")
    assert run(intcode).output == [204]
    intcode = get_intcode_from_string("109,1,209,-1,204,-106,99")
    assert run(intcode).output == [204]
    intcode = get_intcode_from_string("109,1,3,3,204,2,99")
    assert run(intcode, [42]).output == [42]
    assert run(intcode, [314]).output == [314]
    intcode = get_intcode_from_string("109,1,203,2,204,2,99")
    assert run(intcode, [42]).output == [42]
    assert run(intcode, [314]).output == [314]


def run_tests():
    run_tests_day2()
    run_tests_day5()
    run_tests_day7()
    run_tests_day9()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    end = datetime.datetime.now()
    print(end - begin)
