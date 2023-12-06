# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"


def get_elves_from_lines(lines):
    elves = []
    elf = []
    for line in lines:
        if line:
            elf.append(int(line))
        else:
            elves.append(elf)
            elf = []
    if elf:
        elves.append(elf)
    return elves


def get_elves_from_file(file_path=resource_dir + "year2022_day1_input.txt"):
    with open(file_path) as f:
        return get_elves_from_lines([l.strip() for l in f])


def max_elf(elves, nb=1):
    calories = sorted(sum(elf) for elf in elves)
    top = calories[-nb:]
    return sum(top)


def run_tests():
    elves = get_elves_from_lines(
        """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000""".splitlines()
    )
    assert max_elf(elves, 1) == 24000
    assert max_elf(elves, 3) == 45000


def get_solutions():
    elves = get_elves_from_file()
    print(max_elf(elves, 1) == 68467)
    print(max_elf(elves, 3) == 203420)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
