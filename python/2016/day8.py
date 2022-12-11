# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_instructions_from_file(file_path="../../resources/year2016_day8_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def get_screen_display(pixels, width, height):
    lst = []
    for y in range(height):
        lst.append("".join("#" if (x, y) in pixels else "." for x in range(width)))
    return "\n".join(lst)


def apply_instruction(instruction, pixels, width, height):
    instr_lst = instruction.split(" ")
    cmd = instr_lst[0]
    param1 = instr_lst[1]
    if cmd == "rect":
        a, b = param1.split("x")
        return {
            (x % width, y % height) for x in range(int(a)) for y in range(int(b))
        } | pixels
    elif cmd == "rotate":
        a = int(instr_lst[2][2:])
        b = int(instr_lst[4])

        if param1 == "column":
            dx, dy = 0, b
        elif param1 == "row":
            dx, dy = b, 0
        else:
            assert False
        return {
            ((x + dx * (y == a)) % width, (y + dy * (x == a)) % height)
            for (x, y) in pixels
        }
    else:
        assert False


def apply_instructions(instructions, width, height):
    pixels = set()
    for i in instructions:
        pixels = apply_instruction(i, pixels, width, height)
    return pixels


def run_tests():
    instructions = [
        "rect 3x2",
        "rotate column x=1 by 1",
        "rotate row y=0 by 4",
        "rotate column x=1 by 1",
    ]
    assert len(apply_instructions(instructions, width=7, height=3))


def get_solutions():
    instructions = get_instructions_from_file()
    ret = apply_instructions(instructions, width=50, height=6)
    print(len(ret) == 116)
    print(get_screen_display(ret, width=50, height=6) == """\
#..#.###...##....##.####.#....###...##..####.####.
#..#.#..#.#..#....#.#....#....#..#.#..#.#.......#.
#..#.#..#.#..#....#.###..#....###..#....###....#..
#..#.###..#..#....#.#....#....#..#.#....#.....#...
#..#.#....#..#.#..#.#....#....#..#.#..#.#....#....
.##..#.....##...##..#....####.###...##..####.####.""")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
