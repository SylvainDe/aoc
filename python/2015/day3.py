# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_instructions_from_file(file_path="../../resources/year2015_day3_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


directions = {
    "<": (-1, 0),  # West
    ">": (1, 0),  # East
    "v": (0, -1),  # South
    "^": (0, +1),  # North
}


def get_path(instructions):
    x, y = 0, 0
    yield x, y
    for ins in instructions:
        dx, dy = directions[ins]
        x += dx
        y += dy
        yield x, y


def get_nb_houses(instructions):
    return len(set(get_path(instructions)))


def get_nb_houses_with_robo(instructions):
    ins1, ins2 = instructions[1::2], instructions[0::2]
    return len(set(get_path(ins1)) | set(get_path(ins2)))


def run_tests():
    assert get_nb_houses(">") == 2
    assert get_nb_houses("^>v<") == 4
    assert get_nb_houses("^v^v^v^v^v") == 2
    assert get_nb_houses_with_robo("^v") == 3
    assert get_nb_houses_with_robo("^>v<") == 3
    assert get_nb_houses_with_robo("^v^v^v^v^v") == 11


def get_solutions():
    instructions = get_instructions_from_file()
    print(get_nb_houses(instructions) == 2081)
    print(get_nb_houses_with_robo(instructions) == 2341)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
