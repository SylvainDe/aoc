# vi: set shiftwidth=4 tabstop=4 expandtab:

nb_days = 9
days = [__import__("day%d" % i) for i in range(1, nb_days + 1)]


def run_tests():
    print("Unit-tests")
    for day in days:
        print("-", day.__name__)
        day.run_tests()
    print()


def get_solutions():
    print("Actual solutions")
    for day in days:
        print("-", day.__name__)
        day.get_solutions()
    print()


if __name__ == "__main__":
    run_tests()
    get_solutions()
