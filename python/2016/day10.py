# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import re
import collections


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_instructions_from_file(
    file_path=top_dir + "resources/year2016_day10_input.txt",
):
    with open(file_path) as f:
        return [l.strip() for l in f]


value_goes_re = r"value (\d+) goes to bot (\d+)"
bot_gives_re = r"bot (\d+) gives low to ([a-z]+) (\d+) and high to ([a-z]+) (\d+)"


def parse_instructions(instructions):
    bot_chips = dict()
    rules = dict()
    for instruction in instructions:
        match = re.match(value_goes_re, instruction)
        if match:
            val, bot = match.groups()
            bot_chips.setdefault(int(bot), []).append(int(val))
        else:
            match = re.match(bot_gives_re, instruction)
            if match:
                bot, low_type, low_nb, high_type, high_nb = match.groups()
                bot_int = int(bot)
                assert bot_int not in rules
                rules[bot_int] = ((low_type, int(low_nb)), (high_type, int(high_nb)))
            else:
                assert False
    return bot_chips, rules


def follow_instructions(instructions):
    bot_chips, rules = parse_instructions(instructions)
    bots_to_action = collections.deque(
        [bot for bot, chip_lst in bot_chips.items() if len(chip_lst) > 1]
    )
    outputs = dict()
    comparisons = []
    while bots_to_action:
        bot_nb = bots_to_action.popleft()
        low_rule, high_rule = rules[bot_nb]
        low, high = sorted(bot_chips.pop(bot_nb))
        comparisons.append((bot_nb, low, high))
        for c, (dest_type, dest_nb) in [(low, low_rule), (high, high_rule)]:
            if dest_type == "output":
                outputs.setdefault(dest_nb, []).append(c)
            elif dest_type == "bot":
                l = bot_chips.setdefault(dest_nb, [])
                l.append(c)
                if len(l) > 1:
                    bots_to_action.append(dest_nb)
            else:
                assert False
    return comparisons, outputs


def run_tests():
    instructions = [
        "value 5 goes to bot 2",
        "bot 2 gives low to bot 1 and high to bot 0",
        "value 3 goes to bot 1",
        "bot 1 gives low to output 1 and high to bot 0",
        "bot 0 gives low to output 2 and high to output 0",
        "value 2 goes to bot 2",
    ]
    comp, out = follow_instructions(instructions)
    assert comp == [(2, 2, 5), (1, 2, 3), (0, 3, 5)]
    assert out == {1: [2], 2: [3], 0: [5]}


def get_solutions():
    instructions = get_instructions_from_file()
    comp, out = follow_instructions(instructions)
    for bot, low, high in comp:
        if (low, high) == (17, 61):
            print(bot == 101)
            break
    else:
        assert False
    mult = 1
    for chips in [out[0], out[1], out[2]]:
        (val,) = chips
        mult *= val
    print(mult == 37789)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
