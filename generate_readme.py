"""Script to generate README.

Usage: python3 generate_readme.py > README.md
"""
import os
import re

# Separator
sep = "|"

# URLs
puzzle_url = "[Problem](https://adventofcode.com/{year}/day/{day})"
input_url = "[Input](https://adventofcode.com/{year}/day/{day}/input)"
stats_url = "[Stats](https://adventofcode.com/{year}/leaderboard/self)"

# Local files
puzzle_file = "resources/year{year}_day{day}_puzzle.txt"
input_file = "resources/year{year}_day{day}_input.txt"
python_file = "python/{year}/day{day}.py"
rust_file = "rust/src/{year}/day{day}/main.rs"
stats_file = "misc/leaderboard_self_{year}.txt"

# Header
header = """# aoc

Solutions for Advent Of Code

Solutions used to be stored in different repositories for each year limiting the code reuse:
 - https://github.com/SylvainDe/aoc2019
 - https://github.com/SylvainDe/aoc2020
 - https://github.com/SylvainDe/aoc2021

Solutions are written in Python and/or Rust.
"""

# Ranges
year_range = reversed(range(2015, 2022+1))
day_range = range(1, 25+1)


def file_contains(filepath, string):
    with open(filepath) as f:
        for line in f:
            if string in line:
                return True
    return False


def format_file(filepath):
    if not os.path.isfile(filepath):
        return ""
    name_shown = os.path.basename(filepath)
    if filepath.endswith("puzzle.txt"):
        name_shown = "puzzle.txt"
    elif filepath.endswith("input.txt"):
        name_shown = "input.txt"
    elif filepath.startswith("misc/leaderboard_self_"):
        name_shown = "stats.txt"
    elif filepath.endswith(".py") and file_contains(filepath, "xxx = get_xxx_from_file"):
        name_shown = "-"
    elif filepath.endswith(".rs") and file_contains(filepath, "fn part1(_arg"):
        name_shown = "-"
    return "[{name_shown}]({fullpath})".format(name_shown=name_shown, fullpath=filepath)

def format_table_colums(columns):
    return "{}{}{}".format(sep, sep.join(columns), sep)


class YearData():
    def __init__(self, year):
        self.year = year
        self.stats_url = self.format_str(stats_url)
        self.stats_file = self.format_str(stats_file)
        try:
            stats = self.extract_stats()
        except FileNotFoundError:
            stats = dict()
        days = [DayData(year, day, stats.get(day, dict())) for day in day_range]
        self.days = [d for d in days if d.is_valid()]
        self.nb_stars = sum(d.nb_stars for d in days)

    def __str__(self):
        return self.format_str("Year {year}")

    def is_valid(self):
        # Any condition can be imagined here (for instance nb of stars)
        return self.days

    def format_str(self, s):
        return s.format(year=self.year)

    def extract_stats(self):
        time_re = r"([0-9:]+|&gt;24h|-)"
        rank_re = r"(\d+|-)"
        score_re = r"(\d+|-)"
        stat_line_re = re.compile(
            r"^\s+(?P<day>\d+)" \
             "\s+(?P<time1>%s)\s+(?P<rank1>%s)\s+(?P<score1>%s)"
             "\s+(?P<time2>%s)\s+(?P<rank2>%s)\s+(?P<score2>%s)$"
            % (time_re, rank_re, score_re, time_re, rank_re, score_re)
        )
        all_stats = dict()
        with open(self.stats_file) as f:
            for line in f:
                m = stat_line_re.match(line)
                if m is None:
                    continue
                gd = m.groupdict()
                day = int(gd["day"])
                stats = dict()
                for suff in ("1", "2"):
                    time, rank, score = gd["time" + suff], gd["rank" + suff], gd["score" + suff]
                    assert (rank == "-") == (time == "-") == (score == "-")
                    if rank != "-":
                        stats["time" + suff] = time.replace("&gt;", "+")
                        stats["rank" + suff] = int(rank)
                        stats["score" + suff] = int(score)
                all_stats[day] = stats
        return all_stats

    def get_columns(self):
        return [
            str(self),
            self.stats_url,
            format_file(self.stats_file),
            str(self.nb_stars),
            "-",
            "-",
            "-",
            "-"
        ]

class DayData():
    def __init__(self, year, day, stats):
        self.year = year
        self.day = day
        self.puzzle_url = self.format_str(puzzle_url)
        self.input_url = self.format_str(input_url)
        self.puzzle_file = self.format_str(puzzle_file)
        self.input_file = self.format_str(input_file)
        self.python_file = self.format_str(python_file)
        self.rust_file = self.format_str(rust_file)
        self.nb_stars = 0
        self.part1_time = stats.get("time1")
        self.part2_time = stats.get("time2")
        self.part1_rank = stats.get("rank1")
        self.part2_rank = stats.get("rank2")
        self.part1_score = stats.get("score1")
        self.part2_score = stats.get("score2")
        assert (self.part1_time is None) == (self.part1_rank is None) == (self.part1_score is None)
        assert (self.part2_time is None) == (self.part2_rank is None) == (self.part2_score is None)
        self.nb_stars = (self.part1_time is not None) + (self.part2_time is not None)

    def __str__(self):
        return self.format_str("{year}/{day}")

    def is_valid(self):
        # Any condition can be imagined here (for instance nb of stars)
        return any(os.path.isfile(f) for f in (self.puzzle_file, self.input_file, self.python_file, self.rust_file))

    def format_str(self, s):
        return s.format(year=self.year, day=self.day)

    def get_columns(self):
        return [
            str(self),
            self.puzzle_url + " " + self.input_url,
            format_file(self.puzzle_file) + " " + format_file(self.input_file),
            "*" * self.nb_stars,
            format_file(self.python_file),
            format_file(self.rust_file),
            "-" if self.part1_time is None else self.part1_time,
            "-" if self.part2_time is None else self.part2_time,
        ]


# Collect data
years = [YearData(year) for year in year_range]
years = [y for y in years if y.is_valid()]
total_star_count = sum(y.nb_stars for y in years)

# Format data
print(header)
columns = ["Date", "URLs", "Puzzle & Input", "Stars", "Python", "Rust", "Time part 1", "Time part 2"]
for y in years:
    print("## " + str(y))
    print(format_table_colums(columns))
    print(format_table_colums(("---" for _ in columns)))
    for d in y.days:
        print(format_table_colums(d.get_columns()))
    print(format_table_colums(y.get_columns()))
    print()
print("##  Total")
for y in years:
    print("{year}: {nb_stars} {stars}".format(year=y, nb_stars=y.nb_stars, stars="*"*y.nb_stars))
print("Total:    {nb_stars}".format(nb_stars=total_star_count))

