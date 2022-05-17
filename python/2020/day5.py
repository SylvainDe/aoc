# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_seat_ids_from_file(file_path="../../resources/year2020_day5_input.txt"):
    with open(file_path) as f:
        return set([get_seat_id_from_boarding_pass(l.strip()) for l in f])


def get_seat_id_from_boarding_pass(bp):
    trans_table = str.maketrans("FBLR", "0101")
    binary_bp = bp.translate(trans_table)
    row, col = int(binary_bp[:7], 2), int(binary_bp[7:], 2)
    return row * 8 + col


def get_missing_seat_id(seat_ids):
    for i in seat_ids:
        if (i + 1) not in seat_ids and (i + 2) in seat_ids:
            return i + 1
    return None


def run_tests():
    assert get_seat_id_from_boarding_pass("FBFBBFFRLR") == 357
    assert get_seat_id_from_boarding_pass("BFFFBBFRRR") == 567
    assert get_seat_id_from_boarding_pass("FFFBBBFRRR") == 119
    assert get_seat_id_from_boarding_pass("BBFFBBFRLL") == 820


def get_solutions():
    seat_ids = get_seat_ids_from_file()
    print(max(seat_ids) == 850)
    print(get_missing_seat_id(seat_ids) == 599)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
