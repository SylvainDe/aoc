# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_report_from_line(string):
    return [int(s) for s in string.split()]


def get_reports_from_lines(string):
    return [get_report_from_line(l) for l in string.splitlines()]


def get_reports_from_file(file_path=top_dir + "resources/year2024_day2_input.txt"):
    with open(file_path) as f:
        return get_reports_from_lines(f.read())


def pairwise(iterable):
    # pairwise('ABCDEFG') → AB BC CD DE EF FG

    iterator = iter(iterable)
    a = next(iterator, None)

    for b in iterator:
        yield a, b
        a = b


def is_safe(report):
    return any(sorted(report, reverse=b) == report for b in [True, False]) and all(
        1 <= abs(a - b) <= 3 for a, b in pairwise(report)
    )


def is_safe2(report):
    # Not the most efficient solution
    return any(is_safe(report[:i] + report[i + 1 :]) for i in range(len(report)))


def get_nb_safe_reports(reports):
    return sum(is_safe(r) for r in reports)


def get_nb_safe_reports2(reports):
    return sum(is_safe2(r) for r in reports)


def run_tests():
    reports = get_reports_from_lines(
        """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
    )
    assert get_nb_safe_reports(reports) == 2
    assert get_nb_safe_reports2(reports) == 4


def get_solutions():
    reports = get_reports_from_file()
    print(get_nb_safe_reports(reports) == 411)
    print(get_nb_safe_reports2(reports) == 465)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
