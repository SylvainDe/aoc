# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import collections

SKIP_SLOW = True

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

def get_max_geodes(bp, time=24):
    queue = collections.deque([(time, 0, 0, 0, 0, 1, 0, 0, 0)]) # time, ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot
    max_geode = 0
    seen = set()
    # Compute maximum needs
    max_ore_cost = max(bp.ore_robot_ore, bp.clay_robot_ore, bp.obsidian_robot_ore, bp.geode_robot_ore)
    max_clay_cost = bp.obsidian_robot_clay
    max_obs_cost = bp.geode_robot_obsidian
    # prev_time = None
    while queue:
        state = queue.popleft()
        assert all(v >= 0 for v in state)
        time, ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot = state
        max_geode = max(geode, max_geode)
        if time == 0:
            continue
        # if time != prev_time:
        #     print(bp.id, "time:", time, ":", len(queue), ",", max_geode)
        prev_time = time
        time2 = time - 1
        if state in seen:
            continue
        seen.add(state)
        ore2 = ore + ore_robot
        clay2 = clay + clay_robot
        obsidian2 = obsidian + obsidian_robot
        geode2 = geode + geode_robot
        # First optimisation: do not buy a robot if we produce enough of the corresponding ressource
        # TODO: This is not quite fast enough :(
        queue.append((time2, ore2, clay2, obsidian2, geode2, ore_robot, clay_robot, obsidian_robot, geode_robot))
        if ore_robot < max_ore_cost and ore >= bp.ore_robot_ore:
            queue.append((time2, ore2 - bp.ore_robot_ore, clay2, obsidian2, geode2, ore_robot+1, clay_robot, obsidian_robot, geode_robot))
        if clay_robot < max_clay_cost and ore >= bp.clay_robot_ore:
            queue.append((time2, ore2 - bp.clay_robot_ore, clay2, obsidian2, geode2, ore_robot, clay_robot+1, obsidian_robot, geode_robot))
        if obsidian_robot < max_obs_cost and ore >= bp.obsidian_robot_ore and clay >= bp.obsidian_robot_clay:
            queue.append((time2, ore2 - bp.obsidian_robot_ore, clay2 - bp.obsidian_robot_clay, obsidian2, geode2, ore_robot, clay_robot, obsidian_robot+1, geode_robot))
        if ore >= bp.geode_robot_ore and obsidian >= bp.geode_robot_obsidian:
            queue.append((time2, ore2 - bp.geode_robot_ore, clay2, obsidian2 - bp.geode_robot_obsidian, geode2, ore_robot, clay_robot, obsidian_robot, geode_robot+1))
    return max_geode

def get_quality_level(bp):
    return bp.id * get_max_geodes(bp)

def get_quality_levels(blueprints):
    return sum(get_quality_level(bp) for bp in blueprints)

def run_tests():
    blueprints = get_blueprints_from_lines("""Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""")
    if not SKIP_SLOW:
        assert get_max_geodes(blueprints[0]) == 9
        assert get_max_geodes(blueprints[1]) == 12
        assert get_quality_level(blueprints[0]) == 9
        assert get_quality_level(blueprints[1]) == 24
        assert get_quality_levels(blueprints) == 33

def get_solutions():
    blueprints = get_blueprints_from_file()
    if not SKIP_SLOW:
        print(get_quality_levels(blueprints) == 960)

if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
