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

def get_find_max_geodes(bp, time=24):
    queue = collections.deque([(time, 0, 0, 0, 0, 1, 0, 0, 0)]) # time, ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot
    max_geode = 0
    while queue:
        time, ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot = queue.popleft()
        assert all(v >= 0 for v in (time, ore, clay, obsidian, geode))
        if time == 0:
            max_geode = max(geode, max_geode)
            continue
        time2 = time - 1
        ore += ore_robot
        clay += clay_robot
        obsidian += obsidian_robot
        geode += geode_robot
        # TODO: Optimisation, cut any non-relevant branches in the seach space
        queue.append((time2, ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot))
        ore_rem = ore - bp.ore_robot_ore
        if ore_rem >= 0:
            queue.append((time2, ore_rem, clay, obsidian, geode, ore_robot+1, clay_robot, obsidian_robot, geode_robot))
        ore_rem = ore - bp.clay_robot_ore
        if ore_rem >= 0:
            queue.append((time2, ore_rem, clay, obsidian, geode, ore_robot, clay_robot+1, obsidian_robot, geode_robot))
        ore_rem, clay_rem = ore - bp.obsidian_robot_ore, clay - bp.obsidian_robot_clay
        if ore_rem >= 0 and clay_rem >= 0:
            queue.append((time2, ore_rem, clay_rem, obsidian, geode, ore_robot, clay_robot, obsidian_robot+1, geode_robot))
        ore_rem, obs_rem = ore - bp.geode_robot_ore, obsidian - bp.geode_robot_obsidian
        if ore_rem >= 0 and obs_rem >= 0:
            queue.append((time2, ore_rem, clay, obs_rem, geode, ore_robot, clay_robot, obsidian_robot, geode_robot+1))
    return max_geode

def run_tests():
    blueprints = get_blueprints_from_lines("""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""")
    # print(get_find_max_geodes(blueprints[0], time=4))
    # print(get_find_max_geodes(blueprints[0], time=5))
    # print(get_find_max_geodes(blueprints[0], time=6))
    # print(get_find_max_geodes(blueprints[0], time=7))
    # print(get_find_max_geodes(blueprints[0], time=8))
    # print(get_find_max_geodes(blueprints[0], time=9))
    # print(get_find_max_geodes(blueprints[0], time=10))
    # print(get_find_max_geodes(blueprints[0], time=11))
    # print(get_find_max_geodes(blueprints[0], time=12))
    # print(get_find_max_geodes(blueprints[0], time=13))
    # print(get_find_max_geodes(blueprints[0], time=14))
    # print(get_find_max_geodes(blueprints[0], time=15))
    # print(get_find_max_geodes(blueprints[0], time=16))
    # print(get_find_max_geodes(blueprints[0]))
    # print(get_find_max_geodes(blueprints[1]))


def get_solutions():
    blueprints = get_blueprints_from_file()

if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
