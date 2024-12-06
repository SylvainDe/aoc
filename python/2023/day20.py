# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

OFF, ON = False, True
LOW, HIGH = 0, 1
BUTTON_PRESS = ("button", "broadcaster", LOW)


def get_module_from_line(string):
    sep = " -> "
    name, mid, dests = string.partition(sep)
    assert mid == sep
    dests = dests.split(", ")
    if name[0] in ("%&"):
        return (name[1:], name[0], dests)
    return (name, None, dests)


def get_modules_from_lines(string):
    lst = [get_module_from_line(l) for l in string.splitlines()]
    return {name: (prefix, dests) for name, prefix, dests in lst}


def get_modules_from_file(file_path=top_dir + "resources/year2023_day20_input.txt"):
    with open(file_path) as f:
        return get_modules_from_lines(f.read())


def get_initial_state(modules):
    flipflops, conjunctions, inputs = {}, {}, {}
    for name, (_, dests) in modules.items():
        for d in dests:
            inputs.setdefault(d, []).append(name)
    for name, (prefix, _) in modules.items():
        if prefix == "%":
            flipflops[name] = OFF
        elif prefix == "&":
            conjunctions[name] = {m: LOW for m in inputs[name]}
    return flipflops, conjunctions


def get_generated_pulses(src, module_name, level, modules, flipflops, conjunctions):
    prefix, dests = modules.get(module_name, (None, []))
    if prefix == "%":
        if level == HIGH:
            return
        previous_state = flipflops[module_name]
        assert previous_state in (ON, OFF)
        flipflops[module_name] = OFF if previous_state == ON else ON
        level_to_send = LOW if previous_state == ON else HIGH
    elif prefix == "&":
        conj = conjunctions[module_name]
        conj[src] = level
        level_to_send = LOW if all(l == HIGH for l in conj.values()) else HIGH
    else:
        assert prefix is None
        level_to_send = level
    assert level_to_send is not None
    for dst in dests:
        new_event = (module_name, dst, level_to_send)
        yield new_event


def process_pulse(modules, input_event, nb=1):
    count = collections.Counter()
    flipflops, conjunctions = get_initial_state(modules)
    d = collections.deque()
    for _ in range(nb):
        d.append(input_event)
        while d:
            src, module_name, level = d.popleft()
            count[level] += 1
            d.extend(
                get_generated_pulses(
                    src, module_name, level, modules, flipflops, conjunctions
                )
            )
    return count[LOW] * count[HIGH]


def run_tests():
    modules = get_modules_from_lines(
        """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
    )
    for nb_rep in (1, 2, 1000):
        assert process_pulse(modules, BUTTON_PRESS, nb_rep) == (nb_rep * 8) * (
            nb_rep * 4
        )
    modules = get_modules_from_lines(
        """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
    )
    assert process_pulse(modules, BUTTON_PRESS, 1) == 4 * 4
    assert process_pulse(modules, BUTTON_PRESS, 2) == 8 * 6
    assert process_pulse(modules, BUTTON_PRESS, 3) == 13 * 9
    assert process_pulse(modules, BUTTON_PRESS, 1000) == 4250 * 2750


def get_solutions():
    modules = get_modules_from_file()
    print(process_pulse(modules, BUTTON_PRESS, 1000) == 818723272)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
