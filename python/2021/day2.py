# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_commands_from_file(file_path="day2_input.txt"):
    with open(file_path) as f:
        return [l.strip().split() for l in f]


def get_final_position(commands):
    hor, depth = 0, 0
    for c, n in commands:
        n = int(n)
        if c == "forward":
            hor += n
        elif c == "down":
            depth += n
        else:
            assert c == "up"
            depth -= n
    return hor * depth


def get_final_position2(commands):
    hor, depth, aim = 0, 0, 0
    for c, n in commands:
        n = int(n)
        if c == "forward":
            hor += n
            depth += n * aim
        elif c == "down":
            aim += n
        else:
            assert c == "up"
            aim -= n
    return hor * depth


def run_tests():
    commands = [
        ["forward", "5"],
        ["down", "5"],
        ["forward", "8"],
        ["up", "3"],
        ["down", "8"],
        ["forward", "2"],
    ]
    assert get_final_position(commands) == 150
    assert get_final_position2(commands) == 900


def get_solutions():
    commands = get_commands_from_file()
    print(get_final_position(commands))
    print(get_final_position2(commands))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
