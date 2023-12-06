# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections
import heapq


resource_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../resources/"

Player = collections.namedtuple("Player", ["hit_points", "damage", "armor"])
Equipment = collections.namedtuple("Equipment", ["cost", "damage", "armor", "type"])
WEAPON, ARMOR, RING = 1, 2, 3


def get_player_from_lines(string):
    return Player(*[int(l.split(" ")[-1]) for l in string.splitlines()])


def get_player_from_file(file_path=resource_dir + "year2015_day21_input.txt"):
    with open(file_path) as f:
        return get_player_from_lines(f.read())


#         Cost   Damage   Armor  Weapons:
weapons = [
    Equipment(8, 4, 0, WEAPON),  # Dagger
    Equipment(10, 5, 0, WEAPON),  # Shortsword
    Equipment(25, 6, 0, WEAPON),  # Warhammer
    Equipment(40, 7, 0, WEAPON),  # Longsword
    Equipment(74, 8, 0, WEAPON),  # Greataxe
]
#         Cost   Damage   Armor, Armor:
armors = [
    Equipment(13, 0, 1, ARMOR),  # Leather
    Equipment(31, 0, 2, ARMOR),  # Chainmail
    Equipment(53, 0, 3, ARMOR),  # Splintmail
    Equipment(75, 0, 4, ARMOR),  # Bandedmail
    Equipment(102, 0, 5, ARMOR),  # Platemail
]
#         Cost   Damage   Armor, Rings:
rings = [
    Equipment(25, 1, 0, RING),  # Damage +1
    Equipment(50, 2, 0, RING),  # Damage +2
    Equipment(100, 3, 0, RING),  # Damage +3
    Equipment(20, 0, 1, RING),  # Defense +1
    Equipment(40, 0, 2, RING),  # Defense +2
    Equipment(80, 0, 3, RING),  # Defense +3
]


def win_fight(p1, p2):
    damage_to_p2 = max(p1.damage - p2.armor, 1)
    damage_to_p1 = max(p2.damage - p1.armor, 1)
    turn_to_kill_p1, r = divmod(p1.hit_points, damage_to_p1)
    if r:
        turn_to_kill_p1 += 1
    turn_to_kill_p2, r = divmod(p2.hit_points, damage_to_p2)
    if r:
        turn_to_kill_p2 += 1
    return turn_to_kill_p1 >= turn_to_kill_p2


def get_possible_states(has_weapon, has_armor, rings_tuple):
    if not has_weapon:
        for e in weapons:
            yield e, True, has_armor, rings_tuple
        return  # Equip mandatory weapon before anything else
    if not has_armor:
        for e in armors:
            yield e, has_weapon, True, rings_tuple
    if len(rings_tuple) < 2:
        rings_lst = list(rings_tuple)
        for i, e in enumerate(rings):
            if all(i > r for r in rings_tuple):
                yield e, has_weapon, has_armor, tuple(rings_lst + [i])


def least_gold_to_win(boss):
    heap = [
        (0, 0, 0, False, False, ())
    ]  # Money spent, damage, armor, has weapon, has armor, rings
    while heap:
        money, damage, armor, has_weapon, has_armor, rings_tuple = heapq.heappop(heap)
        if win_fight(Player(100, damage, armor), boss):
            return money
        for e, has_weapon2, has_armor2, rings_tuple2 in get_possible_states(
            has_weapon, has_armor, rings_tuple
        ):
            heapq.heappush(
                heap,
                (
                    money + e.cost,
                    damage + e.damage,
                    armor + e.armor,
                    has_weapon2,
                    has_armor2,
                    rings_tuple2,
                ),
            )
    return None


def most_gold_to_lose(boss):
    heap = [
        (0, 0, 0, False, False, ())
    ]  # -Money spent, damage, armor, has weapon, has armor, rings
    most_gold_so_far = 0
    while heap:
        n_money, damage, armor, has_weapon, has_armor, rings_tuple = heapq.heappop(heap)
        if not win_fight(Player(100, damage, armor), boss):
            money = -n_money
            if money > most_gold_so_far:
                most_gold_so_far = money
            for e, has_weapon2, has_armor2, rings_tuple2 in get_possible_states(
                has_weapon, has_armor, rings_tuple
            ):
                heapq.heappush(
                    heap,
                    (
                        -(money + e.cost),
                        damage + e.damage,
                        armor + e.armor,
                        has_weapon2,
                        has_armor2,
                        rings_tuple2,
                    ),
                )
    return most_gold_so_far


def run_tests():
    assert win_fight(Player(8, 5, 5), Player(12, 7, 2))


def get_solutions():
    player = get_player_from_file()
    print(least_gold_to_win(player) == 111)
    print(most_gold_to_lose(player) == 188)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
