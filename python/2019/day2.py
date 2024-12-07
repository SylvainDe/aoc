# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import int_code


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def run_tests():
    int_code.run_tests_day2()


def part1(intcode):
    return int_code.run_verb_noun(intcode, 12, 2)


def part2(intcode):
    for verb in range(99 + 1):
        for noun in range(99 + 1):
            if int_code.run_verb_noun(intcode, noun, verb) == 19690720:
                return 100 * noun + verb


def get_solutions():
    intcode = int_code.get_intcode_from_file("../../resources/year2019_day2_input.txt")
    print(part1(intcode) == 5534943)
    print(part2(intcode) == 7603)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
