# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_instruction_from_line(string):
    # Tuple (nb_cycle, added value)
    if string == "noop":
        return (1, 0)
    _, mid, right = string.partition(" ")
    assert mid == " "
    return (2, int(right))


def get_instructions_from_lines(string):
    return [get_instruction_from_line(l) for l in string.splitlines()]


def get_instruction_from_file(file_path=top_dir + "resources/year2022_day10_input.txt"):
    with open(file_path) as f:
        return get_instructions_from_lines(f.read())


def execute(instructions):
    x = 1
    xs = [x]
    for (nb_cycle, val) in instructions:
        xs.extend([x] * nb_cycle)
        x += val
    return xs


def part1(instructions):
    indexed_values = list(enumerate(execute(instructions)))[20::40]
    return sum(i * val for i, val in indexed_values)


def part2(instructions, width=40):
    crt = []
    for i, x in enumerate(execute(instructions)[1:]):
        crt_pos = i % width
        if crt_pos == 0:
            crt.append("\n")
        pixel_in_sprite = abs(crt_pos - x) <= 1
        crt.append("#" if pixel_in_sprite else ".")
    return "".join(crt)


def run_tests():
    instructions = get_instructions_from_lines(
        """noop
addx 3
addx -5"""
    )
    assert execute(instructions) == [1, 1, 1, 1, 4, 4]
    instructions = get_instructions_from_lines(
        """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
    )
    assert part1(instructions) == 13140
    assert (
        part2(instructions)
        == """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""
    )


def get_solutions():
    instructions = get_instruction_from_file()
    print(part1(instructions) == 17180)
    print(
        part2(instructions)
        == """
###..####.#..#.###..###..#....#..#.###..
#..#.#....#..#.#..#.#..#.#....#..#.#..#.
#..#.###..####.#..#.#..#.#....#..#.###..
###..#....#..#.###..###..#....#..#.#..#.
#.#..#....#..#.#....#.#..#....#..#.#..#.
#..#.####.#..#.#....#..#.####..##..###.."""
    )


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
