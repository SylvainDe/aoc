# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import int_code


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

def run_tests():
    int_code.run_tests_day5()


def get_solutions():
    intcode = int_code.get_intcode_from_file("../../resources/year2019_day5_input.txt")
    print(int_code.run_diagnostic(intcode, input_=1) == 9938601)
    print(int_code.run_diagnostic(intcode, input_=5) == 4283952)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
