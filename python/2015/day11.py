# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_password_from_file(file_path=top_dir + "resources/year2015_day11_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip()


def follows_req1(password):
    ords = [ord(c) for c in password]
    for a, b, c in zip(ords, ords[1:], ords[2:]):
        if a + 1 == b and b + 1 == c:
            return True
    return False


forbidden_chars = "iol"


def follows_req2(password):
    return not any(c in forbidden_chars for c in password)


def get_nb_pairs(password):
    pairs = set()
    for a, b in zip(password, password[1:]):
        if a == b:
            pairs.add(a)
    return len(pairs)


def follows_req3(password):
    return get_nb_pairs(password) >= 2


def is_valid(password):
    return follows_req1(password) and follows_req2(password) and follows_req3(password)


def next_letter(c):
    return chr(ord(c) + 1)


def next_password(password):
    begin, end = password[:-1], password[-1]
    return next_password(begin) + "a" if end == "z" else begin + next_letter(end)


def next_valid_password_slow(password):
    while True:
        password = next_password(password)
        if is_valid(password):
            return password


def next_valid_password(password):
    while True:
        password = next_password(password)
        # Quick skip for req 2
        for c in forbidden_chars:
            beg, mid, end = password.partition(c)
            assert beg + mid + end == password
            if mid:
                password = beg + next_letter(mid) + "a" * len(end)
        assert follows_req2(password)
        # Quick skip for req 1
        # To be continued
        # Quick skip for req 3
        # To be continued
        if is_valid(password):
            return password


def run_tests():
    password = "hijklmmn"
    assert follows_req1(password)
    assert not follows_req2(password)
    assert not is_valid(password)
    password = "abbceffg"
    assert not follows_req1(password)
    assert follows_req2(password)
    assert follows_req3(password)
    assert not is_valid(password)
    password = "abbcegjk"
    assert follows_req2(password)
    assert not follows_req3(password)
    assert not is_valid(password)
    assert next_password("xy") == "xz"
    assert next_password("xz") == "ya"
    assert next_password("ya") == "yb"
    assert next_valid_password_slow("abcdefgh") == "abcdffaa"
    assert next_valid_password("ghijklmn") == "ghjaabcc"


def get_solutions():
    password = get_password_from_file()
    p2 = next_valid_password(password)
    print(p2 == "hepxxyzz")
    p3 = next_valid_password(p2)
    print(p3 == "heqaabcc")


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
