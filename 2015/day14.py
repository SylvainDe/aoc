# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import collections

# Example: "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds."
input_re = r"(?P<name>[A-Za-z]+) can fly (?P<speed>\d+) km\/s for (?P<time>\d+) seconds, but then must rest for (?P<rest>\d+) seconds\."

Reindeer = collections.namedtuple("Reindeer", ("name", "speed", "time", "rest"))


def get_reindeer_from_line(s):
    match = re.match(input_re, s)
    d = match.groupdict()
    return Reindeer(d["name"], int(d["speed"]), int(d["time"]), int(d["rest"]))


def get_reindeers_from_file(file_path="day14_input.txt"):
    with open(file_path) as f:
        return [get_reindeer_from_line(l.strip()) for l in f]


def get_distance(reindeer, time):
    cycle = reindeer.time + reindeer.rest
    nb_cycles, remain = divmod(time, cycle)
    time_flying = nb_cycles * reindeer.time + min(remain, reindeer.time)
    return time_flying * reindeer.speed


def get_scores(reindeers, time):
    points = [0] * len(reindeers)
    for t in range(1, time + 1):
        distances = [get_distance(r, t) for r in reindeers]
        max_distance = max(distances)
        for i, d in enumerate(distances):
            if d == max_distance:
                points[i] += 1
    return points


def run_tests():
    reindeers = [
        (
            "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
            14,
            140,
            1120,
        ),
        (
            "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.",
            16,
            160,
            1056,
        ),
    ]
    for s, d1, d10, d1000 in reindeers:
        r = get_reindeer_from_line(s)
        assert get_distance(r, 1) == d1
        assert get_distance(r, 10) == d10
        assert get_distance(r, 1000) == d1000
    reindeers = [get_reindeer_from_line(s) for s, _, _, _ in reindeers]
    assert get_scores(reindeers, 1) == [0, 1]
    assert get_scores(reindeers, 140) == [1, 139]
    assert get_scores(reindeers, 1000) == [312, 689]


def get_solutions():
    reindeers = get_reindeers_from_file()
    print(max(get_distance(r, 2503) for r in reindeers))
    print(max(get_scores(reindeers, 2503)))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
