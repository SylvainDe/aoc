# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_sequence_from_file(file_path="day1_input.txt"):
    with open(file_path) as f:
        for l in f:
            return l.strip().split(", ")


directions = [
    # Rotating clockwise
    (0, 1),  # North
    (1, 0),  # East
    (0, -1),  # South
    (-1, 0),  # West
]

turns = {
    "L": -1,
    "R": +1,
}


def follow_sequence(sequence):
    x, y, direc = 0, 0, 0
    for seq in sequence:
        turn, walk = seq[0], int(seq[1:])
        direc = (direc + turns[turn]) % 4
        dx, dy = directions[direc]
        x += dx * walk
        y += dy * walk
    return x, y


def dist(point):
    x, y = point
    return abs(x) + abs(y)


def run_tests():
    sequence = "R2, L3".split(", ")
    assert follow_sequence(sequence) == (2, 3)
    sequence = "R2, R2, R2".split(", ")
    assert follow_sequence(sequence) == (0, -2)
    sequence = "R5, L5, R5, R3".split(", ")
    assert follow_sequence(sequence) == (10, 2)


def get_solutions():
    sequence = get_sequence_from_file()
    print(dist(follow_sequence(sequence)))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
