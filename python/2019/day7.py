# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import int_code


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def run_tests():
    int_code.run_tests_day7()


def get_solutions():
    intcode = int_code.get_intcode_from_file("../../resources/year2019_day7_input.txt")
    print(int_code.get_circuit_max_output(intcode) == 199988)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
