# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_xxx_from_line(string):
    return string

def get_xxxs_from_lines(string):
    return [get_xxx_from_line(l) for l in string.splitlines()]

def get_xxxs_from_file(file_path="../../resources/year2016_day12_input.txt"):
    with open(file_path) as f:
        return get_xxxs_from_lines(f.read())


def run_tests():
    xxxs = get_xxxs_from_lines("""abc
def
ghi""")


def get_solutions():
    xxxs = get_xxxs_from_file()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
