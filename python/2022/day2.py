# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime


def get_guide_from_str(string):
    return [tuple(l.strip().split(" ")) for l in string.splitlines()]


def get_guide_from_file(file_path="../../resources/year2022_day2_input.txt"):
    with open(file_path) as f:
        return get_guide_from_str(f.read())


SHAPE_SCORE = {
    "A": 1,  # Rock
    "B": 2,  # Paper
    "C": 3,  # Scissors
    "X": 1,  # Rock
    "Y": 2,  # Paper
    "Z": 3,  # Scissors
}

OUTCOME_SCORE = {
    1: 0,  # Loss
    0: 3,  # Draw
    2: 6,  # Win
}


def score1(p1, p2):
    s1, s2 = SHAPE_SCORE[p1], SHAPE_SCORE[p2]
    return s2 + OUTCOME_SCORE[(s1 - s2) % 3]


def part1(guide):
    return sum(score1(*g) for g in guide)


def score2(p, outcome):
    outcome_values = {
        "X": 1,  # Loss
        "Y": 0,  # Draw
        "Z": 2,  # Win
    }
    outcome_val = outcome_values[outcome]
    s2 = (SHAPE_SCORE[p] - outcome_val - 1) % 3 + 1
    return s2 + OUTCOME_SCORE[outcome_val]


def part2(guide):
    return sum(score2(*g) for g in guide)


def run_tests():
    guide = get_guide_from_str(
        """A Y
B X
C Z"""
    )
    assert part1(guide) == 15
    assert part2(guide) == 12


def get_solutions():
    guide = get_guide_from_file()
    print(part1(guide) == 14264)
    print(part2(guide) == 12382)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
