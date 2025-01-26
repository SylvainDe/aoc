# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


# Example: "Generator A starts with 42"
gen_re = re.compile(r"Generator (?P<name>.*) starts with (?P<value>\d+)")


def generator(name, n):
    factor = 16807 if name == "A" else 48271
    while True:
        n *= factor
        n %= 2147483647
        yield n


def get_generator_from_line(string):
    d = gen_re.match(string).groupdict()
    return d["name"], int(d["value"])


def get_generators_from_lines(string):
    return [get_generator_from_line(l) for l in string.splitlines()]


def get_generators_from_file(file_path=top_dir + "resources/year2017_day15_input.txt"):
    with open(file_path) as f:
        return get_generators_from_lines(f.read())


def run_tests():
    generator_values = get_generators_from_lines(
        """Generator A starts with 65
Generator B starts with 8921"""
    )


def get_solutions():
    generator_values = get_generators_from_file()


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
