# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import itertools
import collections


def get_position_from_line(s):
    return int(s.split(": ")[-1])


def get_positions_from_file(file_path="day21_input.txt"):
    with open(file_path) as f:
        return [get_position_from_line(l.strip()) for l in f]


def deterministic_dice(sides):
    while True:
        for i in range(sides):
            yield i + 1


def get_sum_rolls(dice, n):
    return sum(next(dice) for _ in range(n))


def game(positions, final_score=1000, rolls=3, sides=100):
    nb_player = len(positions)
    # Shift positions by 1 to go from [1, 10] to [0, 9]
    players = [(pos - 1, 0) for pos in positions]
    dice = deterministic_dice(100)
    for i in itertools.count():
        player = i % nb_player
        pos, score = players[player]
        pos += get_sum_rolls(dice, rolls)
        pos %= 10
        score += pos + 1  # Shift position back to compute score
        players[player] = (pos, score)
        if score >= final_score:
            nb_rolls = rolls * (i + 1)
            return min([s for p, s in players]) * nb_rolls


def get_sum_quantum_dice(sides, nb_rolls):
    count = collections.Counter([0])
    for _ in range(nb_rolls):
        count2 = collections.Counter()
        for val, nb in count.items():
            for s in range(sides):
                count2[val + s + 1] += nb
        count = count2
    return count


def game2(positions, final_score=21, rolls=3, sides=3):
    nb_player = len(positions)
    nb_wins = [0 for _ in positions]
    # Shift positions by 1 to go from [1, 10] to [0, 9]
    players = [(pos - 1, 0) for pos in positions]
    # Store games in a counter to handle multiple games at once
    ongoing_games = collections.Counter([(tuple(players), 0)])
    # Compute properties of dice just once
    dice_count = get_sum_quantum_dice(sides, rolls)
    while ongoing_games:
        ongoing_games2 = collections.Counter()
        for game, count in ongoing_games.items():
            players, player_idx = game
            player = players[player_idx]
            next_player_idx = (player_idx + 1) % nb_player
            for val, count2 in dice_count.items():
                count3 = count * count2
                pos, score = player
                pos += val
                pos %= 10
                score += pos + 1  # Shift position back to compute score
                if score >= final_score:
                    nb_wins[player_idx] += count3
                else:
                    players_lst = list(players)
                    players_lst[player_idx] = (pos, score)
                    ongoing_games2[(tuple(players_lst), next_player_idx)] += count3
        ongoing_games = ongoing_games2
    return max(nb_wins)


def run_tests():
    positions = [4, 8]
    assert game(positions) == 739785
    assert game2(positions) == 444356092776315


def get_solutions():
    positions = get_positions_from_file()
    print(game(positions))
    print(game2(positions))


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
