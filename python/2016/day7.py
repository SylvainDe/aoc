# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_ip_from_file(file_path="../../resources/year2016_day7_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def support_tls(ip):
    is_in_bracket = False
    abba_found = False
    for a, b, c, d in zip(ip, ip[1:], ip[2:], ip[3:]):
        if a == "[":
            is_in_bracket = True
        elif a == "]":
            is_in_bracket = False
        elif a != b and a == d and b == c:
            if is_in_bracket:
                return False
            else:
                abba_found = True
    return abba_found


def support_ssl(ip):
    is_in_bracket = False
    abas, babs = set(), set()
    for a, b, c in zip(ip, ip[1:], ip[2:]):
        if a == "[":
            is_in_bracket = True
        elif a == "]":
            is_in_bracket = False
        elif a != b and a == c and b not in "[]":
            if is_in_bracket:
                babs.add(b + a)
            else:
                abas.add(a + b)
    return len(set.intersection(abas, babs)) > 0


def run_tests():
    assert support_tls("abba[mnop]qrst")
    assert not support_tls("abcd[bddb]xyyx")
    assert not support_tls("aaaa[qwer]tyui")
    assert support_tls("ioxxoj[asdfgh]zxcvbn")
    assert support_ssl("aba[bab]xyz")
    assert not support_ssl("xyx[xyx]xyx")
    assert support_ssl("aaa[kek]eke")
    assert support_ssl("zazbz[bzb]cdb")


def get_solutions():
    ips = get_ip_from_file()
    print(sum(support_tls(ip) for ip in ips) == 105)
    print(sum(support_ssl(ip) for ip in ips) == 258)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
