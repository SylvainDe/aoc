# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_modules_from_file(file_path="day1_input.txt"):
    with open(file_path) as f:
        return [int(l.strip()) for l in f]


def get_fuel_requirement(weight):
    return (weight // 3) - 2


def get_fuel_requirement2(weight):
    ret = 0
    while True:
        weight = (weight // 3) - 2
        if weight <= 0:
            break
        ret += weight
    return ret


def get_full_fuel_requirement(modules):
    return sum(get_fuel_requirement(m) for m in modules)


def get_full_fuel_requirement2(modules):
    return sum(get_fuel_requirement2(m) for m in modules)


def run_tests():
    modules = [12, 14, 1969, 100756]
    assert get_full_fuel_requirement(modules) == 2 + 2 + 654 + 33583
    assert get_full_fuel_requirement2(modules) == 2 + 2 + 966 + 50346


def get_solutions():
    modules = get_modules_from_file()
    print(get_full_fuel_requirement(modules))
    print(get_full_fuel_requirement2(modules))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
