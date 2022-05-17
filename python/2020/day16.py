# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import re

rules_re = re.compile(r"(?P<min>\d+)-(?P<max>\d+)")


def get_rule_from_string(string):
    name, values = string.split(": ")
    return (name, [(int(mini), int(maxi)) for mini, maxi in rules_re.findall(values)])


def get_ticket_from_string(string):
    return [int(n) for n in string.split(",")]


def get_info_from_string(string):
    rules, ticket, tickets = string.split("\n\n")
    return (
        [get_rule_from_string(r) for r in rules.splitlines()],
        get_ticket_from_string(ticket.splitlines()[1]),
        [get_ticket_from_string(s) for s in tickets.splitlines()[1:] if s],
    )


def get_info_from_file(file_path="../../resources/year2020_day16_input.txt"):
    with open(file_path) as f:
        return get_info_from_string(f.read())


def value_valid_for_a_field(rules, n):
    return any(mini <= n <= maxi for _, lst in rules for mini, maxi in lst)


def validity_rate(rules, tickets):
    return sum(n for t in tickets for n in t if not value_valid_for_a_field(rules, n))


def guess_field_position(rules, tickets):
    positions = set(range(len(tickets[0])))
    impossible_positions = {name: set() for name, _ in rules}
    for t in tickets:
        # Only valid tickets
        if all(value_valid_for_a_field(rules, n) for n in t):
            for i, n in enumerate(t):
                for name, lst in rules:
                    if not any(mini <= n <= maxi for (mini, maxi) in lst):
                        impossible_positions[name].add(i)
    return guess_positions(impossible_positions, positions)


def guess_positions(impossible_positions, positions):
    found = dict()
    while impossible_positions:
        for name, imposs in impossible_positions.items():
            possible = positions - imposs
            if len(possible) == 0:
                print("Impossible")
                return None
            elif len(possible) == 1:
                unique_pos = possible.pop()
                found[name] = unique_pos
                del impossible_positions[name]
                for name, imposs in impossible_positions.items():
                    imposs.add(unique_pos)
                break
        else:
            # TODO
            print("No change")
            return None
    return found


def run_tests():
    example1 = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""
    rules, ticket, tickets = get_info_from_string(example1)
    assert rules == [
        ("class", [(1, 3), (5, 7)]),
        ("row", [(6, 11), (33, 44)]),
        ("seat", [(13, 40), (45, 50)]),
    ]
    assert ticket == [7, 1, 14]
    assert tickets == [[7, 3, 47], [40, 4, 50], [55, 2, 20], [38, 6, 12]]
    assert validity_rate(rules, tickets)

    example2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9"""
    rules, ticket, tickets = get_info_from_string(example2)
    assert guess_field_position(rules, tickets) == {"seat": 2, "class": 1, "row": 0}


def get_solutions():
    rules, ticket, tickets = get_info_from_file()
    print(validity_rate(rules, tickets) == 26053)
    mult = 1
    field_position = guess_field_position(rules, tickets)
    for field, idx in field_position.items():
        if field.startswith("departure"):
            mult *= ticket[idx]
    print(mult == 1515506256421)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
