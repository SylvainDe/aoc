# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_xxx_from_file(file_path="../../resources/year2018_day17_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def run_tests():
    xxx = ""


def get_solutions():
    xxx = get_xxx_from_file()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
