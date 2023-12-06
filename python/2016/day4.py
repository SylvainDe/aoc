# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re
import collections
import string


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

Room = collections.namedtuple("Room", ("name", "sector", "checksum"))

# Example: aaaaa-bbb-z-y-x-123[abxyz]
room_re = r"(?P<name>[a-z-]+)-(?P<sector>[0-9]+)\[(?P<checksum>.*)\]"


def get_room_from_string(s):
    match = re.match(room_re, s)
    d = match.groupdict()
    return Room(d["name"], int(d["sector"]), d["checksum"])


def get_rooms_from_file(file_path=resource_dir + "year2016_day4_input.txt"):
    with open(file_path) as f:
        return [get_room_from_string(l.strip()) for l in f]


def get_checksum(name):
    groups = []
    prev_n = None
    for d, n in collections.Counter(name).most_common():
        if d != "-":
            if prev_n != n:
                groups.append([])
            groups[-1].append(d)
            prev_n = n
    check = "".join("".join(sorted(g)) for g in groups)
    return check[:5]


def is_real(room):
    return get_checksum(room.name) == room.checksum


def caesar_cipher(n):
    az = string.ascii_lowercase
    shift = n % len(az)
    return str.maketrans(az + "-", az[shift:] + az[:shift] + " ")


def decrypt_name(room):
    return room.name.translate(caesar_cipher(room.sector))


def run_tests():
    assert is_real(get_room_from_string("aaaaa-bbb-z-y-x-123[abxyz]"))
    assert is_real(get_room_from_string("a-b-c-d-e-f-g-h-987[abcde]"))
    assert is_real(get_room_from_string("not-a-real-room-404[oarel]"))
    assert not is_real(get_room_from_string("totally-real-room-200[decoy]"))


def get_solutions():
    rooms = get_rooms_from_file()
    print(sum(room.sector for room in rooms if is_real(room)) == 245102)
    for room in rooms:
        d = decrypt_name(room)
        if "north" in d:
            print(room.sector == 324)
            break
    else:
        assert False


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
