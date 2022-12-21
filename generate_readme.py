"""Script to generate README.

Usage: python3 generate_readme.py
"""
import os
import re

# URLs
aoc="[Advent of Code](https://adventofcode.com)"
puzzle_url = "[Problem](https://adventofcode.com/{year}/day/{day})"
input_url = "[Input](https://adventofcode.com/{year}/day/{day}/input)"
event_url = "[{year}](https://adventofcode.com/{year})"
stats_url = "[Stats](https://adventofcode.com/{year}/leaderboard/self)"

# Local files
puzzle_file = "resources/year{year}_day{day}_puzzle.html"
input_file = "resources/year{year}_day{day}_input.txt"
python_file = "python/{year}/day{day}.py"
rust_file = "rust/src/{year}/day{day}.rs"
stats_file = "misc/leaderboard_self_{year}.html"

# Ranges
year_range = range(2015, 2022+1)
day_range = range(1, 25+1)


def file_contains(filepath, string):
    with open(filepath) as f:
        return any(string in line for line in f)
    return False


def format_file(filepath):
    if not os.path.isfile(filepath):
        return ""
    name_shown = os.path.basename(filepath)
    if filepath.endswith("puzzle.html"):
        name_shown = "puzzle.html"
    elif filepath.endswith("input.txt"):
        name_shown = "input.txt"
    elif filepath.startswith("misc/leaderboard_self_"):
        name_shown = "stats.txt"
    elif filepath.endswith(".py") and file_contains(filepath, "def get_xxx_from_line"):
        name_shown = "-"
    elif filepath.endswith(".rs") and file_contains(filepath, "fn part1(_arg"):
        name_shown = "-"
    return "[{name_shown}]({fullpath})".format(name_shown=name_shown, fullpath=filepath)


class YearData():
    def __init__(self, year):
        self.year = year
        self.stats_url = self.format_str(stats_url)
        self.stats_file = self.format_str(stats_file)
        self.event_url = self.format_str(event_url)
        try:
            stats = self.extract_stats()
        except FileNotFoundError:
            stats = dict()
        days = [DayData(year, day, stats.get(day, dict())) for day in day_range]
        self.days = [d for d in days if d.is_valid()]
        self.nb_stars = sum(d.nb_stars for d in days)

    def __str__(self):
        return self.event_url

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


class DayData():
    def __init__(self, year, day, stats):
        self.year = year
        self.day = day
        self.puzzle_url = self.format_str(puzzle_url)
        self.input_url = self.format_str(input_url)
        self.puzzle_file = self.format_str(puzzle_file)
        self.input_file = self.format_str(input_file)
        self.title = self.get_title()
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
        return self.title if self.title is not None else self.format_str("{year}/12/{day}")

    def is_valid(self):
        # Any condition can be imagined here (for instance nb of stars)
        return any(os.path.isfile(f) for f in (self.puzzle_file, self.input_file, self.python_file, self.rust_file))

    def format_str(self, s):
        return s.format(year=self.year, day=self.day)

    def get_title(self):
        title_re = re.compile(r".*<article class.*<h2>--- (?P<title>.*) ---<")
        try:
            with open(self.puzzle_file) as f:
                for line in f:
                    m = title_re.match(line)
                    if m is not None:
                        return m.groupdict()["title"]
        except FileNotFoundError:
            pass
        return None

def format_table_colums(columns, sep="|"):
    return "{}{}{}\n".format(sep, sep.join(str(c) for c in columns), sep)


# Header
readme_header = """# aoc

Solutions for {}

Solutions used to be stored in different repositories for each year limiting the code reuse:
 - https://github.com/SylvainDe/aoc2019
 - https://github.com/SylvainDe/aoc2020
 - https://github.com/SylvainDe/aoc2021

Solutions are written in Python and/or Rust.

""".format(aoc)


if __name__ == "__main__":
    import sys
    try:
        destfile = sys.argv[1]
    except IndexError:
        destfile = "README.md"

    ################
    # Collect data #
    ################
    years = [YearData(year) for year in year_range]
    years = [y for y in years if y.is_valid()]

    ################
    # Format data  #
    ################
    with open(destfile, "w") as f:
        f.write(readme_header)

        # Details for each day
        columns = ["Day", "URLs", "Puzzle & Input", "Stars", "Python", "Rust", "Time part 1", "Time part 2"]
        for y in reversed(years):
            f.write("## {}\n".format(y))
            f.write(format_table_colums(columns))
            f.write(format_table_colums(("---" for _ in columns)))
            for d in y.days:
                f.write(format_table_colums([
                    d,
                    "{} {}".format(d.puzzle_url, d.input_url),
                    "{} {}".format(format_file(d.puzzle_file), format_file(d.input_file)),
                    "*" * d.nb_stars,
                    format_file(d.python_file),
                    format_file(d.rust_file),
                    "-" if d.part1_time is None else d.part1_time,
                    "-" if d.part2_time is None else d.part2_time,
                ]))
            f.write(format_table_colums([
                y,
                y.stats_url,
                format_file(y.stats_file),
                y.nb_stars,
                "-",
                "-",
                "-",
                "-"
            ]))
            f.write("\n")

        # Summary of stars
        f.write("##  Summary\n")
        stars_by_day_num = dict()
        for y in years:
            for d in y.days:
                s = d.nb_stars
                stars_by_day_num.setdefault(d.day, dict())[y.year] = s

        columns = ["Day"] + [y for y in years] + ["Total"]
        f.write(format_table_colums(columns))
        f.write(format_table_colums(("---" for _ in columns)))
        for day_num, year_dict in sorted(stars_by_day_num.items()):
            nb_stars = [year_dict.get(y.year, 0) for y in years]
            total = sum(nb_stars)
            values = [day_num] + ["*" * nb for nb in nb_stars] + ["{:2d}: {}".format(total, "*" * total)]
            f.write(format_table_colums(values))
        nb_stars = [y.nb_stars for y in years]
        total = sum(nb_stars)
        values = ["Total"] + nb_stars + [total]
        f.write(format_table_colums(values))
