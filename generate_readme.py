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
years = range(2015, 2021+1)
days = range(1, 25+1)

def file_contains(filepath, string):
    with open(filepath) as f:
        for line in f:
            if string in line:
                return True
    return False


def file_count_lines(filepath, string):
    with open(filepath) as f:
        return sum(string in line for line in f)
    return 0


def format_file(filepath):
    if not os.path.isfile(filepath):
        return ""
    name_shown = os.path.basename(filepath)
    if filepath.endswith("puzzle.txt"):
        name_shown = "puzzle.txt"
    elif filepath.endswith("input.txt"):
        name_shown = "input.txt"
    elif filepath.endswith(".py") and file_contains(filepath, "xxx = get_xxx_from_file"):
        name_shown = "not solved"
    elif filepath.endswith(".rs") and file_contains(filepath, "fn part1(_arg"):
        name_shown = "not solved"
    return "[{name_shown}]({fullpath})".format(name_shown=name_shown, fullpath=filepath)

def format_table_colums(columns):
    return "{}{}{}".format(sep, sep.join(columns), sep)


class YearData():
    def __init__(self, year):
        self.year = year
        self.stats_file = self.format_str(stats_file)
        self.days = {day: DayData(year, day) for day in days}
        self.nb_stars = sum(d.nb_stars for d in self.days.values())
        self.extract_stats()

    def format_str(self, s):
        return s.format(year=self.year)

    def extract_stats(self):
        time_re = r"([0-9:]+|&gt;24h|-)"
        rank_re = r"(\d+|-)"
        score_re = r"(\d+|-)"
        stat_line_re = re.compile(
            r"^\s+(?P<day>\d+)\s+(?P<time1>%s)\s+(?P<rank1>%s)\s+(?P<score1>%s)\s+(?P<time2>%s)\s+(?P<rank2>%s)\s+(?P<score2>%s)$"
            % (time_re, rank_re, score_re, time_re, rank_re, score_re)
        )
        with open(self.stats_file) as f:
            for line in f:
                m = stat_line_re.match(line)
                if m is None:
                    continue
                gd = m.groupdict()
                day = int(gd["day"])
                d = self.days[day]
                time1 = gd["time1"].replace("&gt;", "+")
                time2 = gd["time2"].replace("&gt;", "+")
                rank1 = gd["rank1"]
                rank2 = gd["rank2"]
                score1 = gd["score1"]
                score2 = gd["score2"]
                assert (rank1 == "-") == (time1 == "-") == (score1 == "-") == False
                d.part1_time = time1
                d.part1_rank = rank1
                d.part1_score = score1
                assert (rank2 == "-") == (time2 == "-") == (score2 == "-")
                if rank2 != "-":
                    d.part2_time = time2
                    d.part2_rank = rank2
                    d.part2_score = score2

    def get_columns(self):
        return ["-", "-", "-", str(self.nb_stars), "-", "-", "-", "-"]

class DayData():
    def __init__(self, year, day):
        self.year = year
        self.day = day
        self.puzzle_url = self.format_str(puzzle_url)
        self.input_url = self.format_str(input_url)
        self.puzzle_file = self.format_str(puzzle_file)
        self.input_file = self.format_str(input_file)
        self.python_file = self.format_str(python_file)
        self.rust_file = self.format_str(rust_file)
        self.nb_stars = file_count_lines(self.puzzle_file, "<p>Your puzzle answer was <code>")
        self.part1_time = None
        self.part1_rank = None
        self.part1_score = None
        self.part2_time = None
        self.part2_rank = None
        self.part2_score = None

    def format_str(self, s):
        return s.format(year=self.year, day=self.day)

    def get_columns(self):
        return [
            self.format_str("{year}/{day}"),
            self.puzzle_url + " " + self.input_url,
            format_file(self.puzzle_file) + " " + format_file(self.input_file),
            "*" * self.nb_stars,
            format_file(self.python_file),
            format_file(self.rust_file),
            "-" if self.part1_time is None else self.part1_time,
            "-" if self.part2_time is None else self.part2_time,
        ]


# Collect data
all_years = {year: YearData(year) for year in years}
total_star_count = sum(y.nb_stars for y in all_years.values())

# Format data
print(header)
columns = ["Date", "URLs", "Puzzle & Input", "Stars", "Python", "Rust", "Time part 1", "Time part 2"]
print(format_table_colums(columns))
print(format_table_colums(("---" for _ in columns)))
for year in years:
    y = all_years[year]
    for day in days:
        print(format_table_colums(y.days[day].get_columns()))
    print(format_table_colums(y.get_columns()))
print(format_table_colums(["-", "-", "-", str(total_star_count), "-", "-", "-", "-"]))

