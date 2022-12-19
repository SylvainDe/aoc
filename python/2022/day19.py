# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import collections

# Blueprint 1: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 18 clay. Each geode robot costs 3 ore and 8 obsidian.
blueprint_re = re.compile("^Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.$")

Blueprint = collections.namedtuple("Blueprint", ["id", "ore_robot_ore", "clay_robot_ore", "obsidian_robot_ore", "obsidian_robot_clay", "geode_robot_ore", "geode_robot_obsidian"])

def get_blueprint_from_line(string):
    return Blueprint(*[int(s) for s in blueprint_re.match(string).groups()])

def get_blueprints_from_lines(string):
    return [get_blueprint_from_line(l) for l in string.splitlines()]

def get_blueprints_from_file(file_path="../../resources/year2022_day19_input.txt"):
    with open(file_path) as f:
        return get_blueprints_from_lines(f.read())

def run_tests():
    blueprints = get_blueprints_from_lines("""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""")


def get_solutions():
    blueprints = get_blueprints_from_file()

if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
