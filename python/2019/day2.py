# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import int_code


def run_tests():
    int_code.run_tests_day2()


def part1(intcode):
    intcode = list(intcode)
    intcode[1] = 12
    intcode[2] = 2
    intcode, _ = int_code.run(intcode)
    return intcode[0]


def part2(intcode):
    for verb in range(99 + 1):
        for noun in range(99 + 1):
            if int_code.run_verb_noun(intcode, noun, verb) == 19690720:
                return 100 * noun + verb


def get_solutions():
    intcode = int_code.get_intcode_from_file("../../resources/year2019_day2_input.txt")
    print(part1(intcode))
    print(part2(intcode))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
