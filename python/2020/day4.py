# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

def get_passport(string):
    data = dict()
    for chunk in string.split():
        key, value = chunk.split(":")
        assert key not in value
        data[key] = value
    return data


def get_passports(string):
    return [get_passport(s) for s in string.split("\n\n")]


def get_passports_from_file(file_path=top_dir + "resources/year2020_day4_input.txt"):
    with open(file_path) as f:
        return get_passports(f.read())


def passport_is_valid1(passport):
    keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    return all(key in passport for key in keys)


def is_int_in_range(string, mini, maxi):
    try:
        i = int(string)
        return mini <= i <= maxi
    except TypeError:
        return False
    except ValueError:
        return False


def is_valid_height(string):
    if string.endswith("cm"):
        return is_int_in_range(string[:-2], 150, 193)
    elif string.endswith("in"):
        return is_int_in_range(string[:-2], 59, 76)
    else:
        return False


HCL_RE = re.compile(r"^#[0-9a-f]{6}$")
COLORS = set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
PID_RE = re.compile(r"^\d{9}$")


def passport_is_valid2(passport):
    criteria = {
        "byr": lambda s: is_int_in_range(s, 1920, 2002),
        "iyr": lambda s: is_int_in_range(s, 2010, 2020),
        "eyr": lambda s: is_int_in_range(s, 2020, 2030),
        "hgt": is_valid_height,
        "hcl": lambda s: bool(HCL_RE.match(s)),
        "ecl": lambda s: s in COLORS,
        "pid": lambda s: bool(PID_RE.match(s)),
    }
    try:
        return all(func(passport[k]) for k, func in criteria.items())
    except KeyError:
        return False


def run_tests():
    example1 = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""
    passports = get_passports(example1)
    assert passport_is_valid1(passports[0])
    assert not passport_is_valid1(passports[1])
    assert passport_is_valid1(passports[2])
    assert not passport_is_valid1(passports[3])
    assert sum(passport_is_valid1(p) for p in passports) == 2

    assert not is_int_in_range(None, 1920, 2020)
    assert not is_int_in_range("", 1920, 2020)
    assert not is_int_in_range("1900", 1920, 2020)
    assert is_int_in_range("1930", 1920, 2020)

    assert not is_valid_height("")
    assert is_valid_height("160cm")
    assert not is_valid_height("195cm")
    assert is_valid_height("60in")
    assert not is_valid_height("80in")
    assert not is_valid_height("42")
    assert not is_valid_height("42ab")

    example2_invalid = """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""
    example2_valid = """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"""
    passports_invalid = get_passports(example2_invalid)
    passports_valid = get_passports(example2_valid)
    for p in passports_valid:
        assert passport_is_valid2(p)
    for p in passports_invalid:
        assert not passport_is_valid2(p)


def get_solutions():
    passports = get_passports_from_file()
    print(sum(passport_is_valid1(p) for p in passports) == 228)
    print(sum(passport_is_valid2(p) for p in passports) == 175)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
