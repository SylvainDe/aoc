# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_numbers_from_line(s):
    return [int(v) for v in s.split()]


def get_spreadsheet_from_file(file_path="day2_input.txt"):
    with open(file_path) as f:
        return [get_numbers_from_line(l.strip()) for l in f]


def get_checksum(spreadsheet):
    return sum(max(l) - min(l) for l in spreadsheet)


def run_tests():
    spreadsheet = [
        "5 1 9 5",
        "7 5 3",
        "2 4 6 8",
    ]
    spreadsheet = [get_numbers_from_line(l) for l in spreadsheet]
    print(get_checksum(spreadsheet))


def get_solutions():
    spreadsheet = get_spreadsheet_from_file()
    print(get_checksum(spreadsheet))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
