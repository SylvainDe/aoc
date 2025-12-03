# vi: set shiftwidth=4 tabstop=4 expandtab:


def get_modules():
    nb_days = 12
    for i in range(1, nb_days + 1):
        try:
            yield __import__("day%d" % i)
        except ModuleNotFoundError:
            pass


def run_tests(days):
    print("Unit-tests")
    for day in days:
        print("-", day.__name__)
        day.run_tests()
    print()


def get_solutions(days):
    print("Actual solutions")
    for day in days:
        print("-", day.__name__)
        day.get_solutions()
    print()


if __name__ == "__main__":
    days = list(get_modules())
    run_tests(days)
    get_solutions(days)
