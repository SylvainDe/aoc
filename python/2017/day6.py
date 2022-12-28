# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_xxx_from_line(string):
    return string


def get_xxx_from_file(file_path="../../resources/year2017_day6_input.txt"):
    with open(file_path) as f:
        for l in f:
            return get_xxx_from_line(l.strip())


def run_tests():
    xxx = get_xxx_from_line("abc")


def get_solutions():
    xxx = get_xxx_from_file()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
