# vi: set shiftwidth=4 tabstop=4 expandtab:

nb_days = 25
days = [__import__("day%d" % i) for i in range(1, nb_days + 1)]


def run_tests():
    for day in days:
        print("-", day.__name__)
        day.run_tests()


def get_solutions():
    for day in days:
        print("-", day.__name__)
        day.get_solutions()


if __name__ == "__main__":
    run_tests()
    get_solutions()
