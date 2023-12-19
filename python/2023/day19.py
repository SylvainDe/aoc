# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_rule_from_string(string):
    l = string.split(":")
    if len(l) == 1:
        condition, dest = None, l[0]
    else:
        condition, dest = l
        name, op, nb = condition[0], condition[1], int(condition[2:])
        assert name in ('xmas')
        assert op in ('<>')
        condition = (name, op, nb)
    return condition, dest

def get_workflow_from_line(string):
    name, rules = string.split("{")
    rules = [get_rule_from_string(s) for s in rules[:-1].split(",")]
    return name, rules

def get_part_from_line(string):
    ratings = (s.split("=") for s in string[1:-1].split(","))
    return {k: int(v) for k, v in ratings}

def get_workflows_and_parts_from_lines(string):
    workflows, parts = string.split("\n\n")
    workflows = dict(get_workflow_from_line(l) for l in workflows.splitlines())
    parts = [get_part_from_line(l) for l in parts.splitlines()]
    return workflows, parts

def get_workflows_and_parts_from_file(file_path=top_dir + "resources/year2023_day19_input.txt"):
    with open(file_path) as f:
        return get_workflows_and_parts_from_lines(f.read())

def evaluate_rule_for_part(rule, part):
    cond, dest = rule
    if cond is None:
        return dest
    name, op, nb = cond
    val = part[name]
    if op == '>':
        big, small = val, nb
    else:
        big, small = nb, val
    return dest if big > small else None

def get_status(part, workflows, start='in'):
    for rule in workflows[start]:
        dest = evaluate_rule_for_part(rule, part)
        if dest is not None:
            if dest in workflows:
                return get_status(part, workflows, dest)
            else:
                assert dest in ('AR')
                return dest

def get_accepted_parts_sum(parts, workflows):
    return sum(sum(p.values()) for p in parts if get_status(p, workflows) == 'A')

def get_nb_accepted_combinations(workflows):
    # TODO:
    # Note: an idea could have been to find the accepted range for each
    # value and multiply the range lengths together but the values are not
    # independant so this will not work (this is the reason why 167409079868000
    # can not be written as the product of 3 smallish numbers)
    pass

def run_tests():
    workflows, parts = get_workflows_and_parts_from_lines(
        """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
    )
    assert get_accepted_parts_sum(parts, workflows) == 19114
    print(get_nb_accepted_combinations(workflows), 167409079868000)

def get_solutions():
    workflows, parts = get_workflows_and_parts_from_file()
    print(get_accepted_parts_sum(parts, workflows) == 406849)
    print(get_nb_accepted_combinations(workflows))

if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
