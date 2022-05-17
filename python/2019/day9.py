# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import int_code


def run_tests():
    int_code.run_tests_day9()


def get_solutions():
    intcode = int_code.get_intcode_from_file("../../resources/year2019_day9_input.txt")
    print(int_code.run(intcode, input_=1)[1])
    print(int_code.run(intcode, input_=2)[1])


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
