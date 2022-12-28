# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re
import collections
import operator
import functools

SKIP_SLOW = True

# Blueprint 1: Each ore robot costs 3 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 18 clay. Each geode robot costs 3 ore and 8 obsidian.
blueprint_re = re.compile(
    r"^Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.$"
)

Blueprint = collections.namedtuple(
    "Blueprint",
    [
        "id",
        "ore_robot_ore",
        "clay_robot_ore",
        "obsidian_robot_ore",
        "obsidian_robot_clay",
        "geode_robot_ore",
        "geode_robot_obsidian",
    ],
)


def get_blueprint_from_line(string):
    return Blueprint(*[int(s) for s in blueprint_re.match(string).groups()])


def get_blueprints_from_lines(string):
    return [get_blueprint_from_line(l) for l in string.splitlines()]


def get_blueprints_from_file(file_path="../../resources/year2022_day19_input.txt"):
    with open(file_path) as f:
        return get_blueprints_from_lines(f.read())


def get_max_geodes(bp, time):
    queue = collections.deque(
        [(time, 0, 0, 0, 0, 1, 0, 0, 0)]
    )  # time, ore, clay, obsidian, geode, ore_robot, clay_robot, obsidian_robot, geode_robot
    max_geode = 0
    seen = set()
    # Compute maximum needs
    max_ore_cost = max(
        bp.ore_robot_ore, bp.clay_robot_ore, bp.obsidian_robot_ore, bp.geode_robot_ore
    )
    max_clay_cost = bp.obsidian_robot_clay
    max_obs_cost = bp.geode_robot_obsidian
    while queue:
        state = queue.popleft()
        assert all(v >= 0 for v in state)
        (
            time,
            ore,
            clay,
            obsidian,
            geode,
            ore_robot,
            clay_robot,
            obsidian_robot,
            geode_robot,
        ) = state
        max_geode = max(geode, max_geode)
        if time == 0:
            continue
        time2 = time - 1
        # Get rid of useless resources
        # Inspired from https://github.com/alexander-yu/adventofcode/blob/master/problems_2022/19.py
        ore = min(ore, max_ore_cost + (max_ore_cost - ore_robot) * time2)
        clay = min(clay, max_clay_cost + (max_clay_cost - clay_robot) * time2)
        obsidian = min(obsidian, max_obs_cost + (max_obs_cost - obsidian_robot) * time2)
        state = (
            time,
            ore,
            clay,
            obsidian,
            geode,
            ore_robot,
            clay_robot,
            obsidian_robot,
            geode_robot,
        )
        if state in seen:
            continue
        seen.add(state)
        ore2 = ore + ore_robot
        clay2 = clay + clay_robot
        obsidian2 = obsidian + obsidian_robot
        geode2 = geode + geode_robot
        # First optimisation: do not buy a robot if we produce enough of the corresponding ressource
        # TODO: This is not quite fast enough :(
        miss_resources = False
        if ore_robot < max_ore_cost:
            if ore >= bp.ore_robot_ore:
                queue.append(
                    (
                        time2,
                        ore2 - bp.ore_robot_ore,
                        clay2,
                        obsidian2,
                        geode2,
                        ore_robot + 1,
                        clay_robot,
                        obsidian_robot,
                        geode_robot,
                    )
                )
            else:
                miss_resources = True
        if clay_robot < max_clay_cost:
            if ore >= bp.clay_robot_ore:
                queue.append(
                    (
                        time2,
                        ore2 - bp.clay_robot_ore,
                        clay2,
                        obsidian2,
                        geode2,
                        ore_robot,
                        clay_robot + 1,
                        obsidian_robot,
                        geode_robot,
                    )
                )
            else:
                miss_resources = True
        if obsidian_robot < max_obs_cost:
            if ore >= bp.obsidian_robot_ore and clay >= bp.obsidian_robot_clay:
                queue.append(
                    (
                        time2,
                        ore2 - bp.obsidian_robot_ore,
                        clay2 - bp.obsidian_robot_clay,
                        obsidian2,
                        geode2,
                        ore_robot,
                        clay_robot,
                        obsidian_robot + 1,
                        geode_robot,
                    )
                )
            else:
                miss_resources = True
        if ore >= bp.geode_robot_ore and obsidian >= bp.geode_robot_obsidian:
            queue.append(
                (
                    time2,
                    ore2 - bp.geode_robot_ore,
                    clay2,
                    obsidian2 - bp.geode_robot_obsidian,
                    geode2,
                    ore_robot,
                    clay_robot,
                    obsidian_robot,
                    geode_robot + 1,
                )
            )
        else:
            miss_resources = True
        if (
            miss_resources
        ):  # Waiting only makes sense if resources are missing to buy something needed
            queue.append(
                (
                    time2,
                    ore2,
                    clay2,
                    obsidian2,
                    geode2,
                    ore_robot,
                    clay_robot,
                    obsidian_robot,
                    geode_robot,
                )
            )

    return max_geode


def get_quality_level(bp):
    return bp.id * get_max_geodes(bp, time=24)


def get_quality_levels(blueprints):
    return sum(get_quality_level(bp) for bp in blueprints)


def mult(iterable, start=1):
    """Returns the product of an iterable - like the sum builtin."""
    return functools.reduce(operator.mul, iterable, start)


def run_tests():
    blueprints = get_blueprints_from_lines(
        """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""
    )
    bp0, bp1 = blueprints
    if not SKIP_SLOW:
        # Shorter tests
        t = 21
        assert get_max_geodes(bp0, t) == 3
        assert get_max_geodes(bp1, t) == 4
        t = 24
        assert get_max_geodes(bp0, t) == 9
        assert get_max_geodes(bp1, t) == 12
        assert get_quality_level(bp0) == 9
        assert get_quality_level(bp1) == 24
        assert get_quality_levels(blueprints) == 33
        t = 32
        assert get_max_geodes(bp0, t) == 56
        assert get_max_geodes(bp1, t) == 62


def get_solutions():
    blueprints = get_blueprints_from_file()
    if not SKIP_SLOW:
        print(get_quality_levels(blueprints) == 960)
        print(mult(get_max_geodes(bp, time=32) for bp in blueprints[:3]) == 2040)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
