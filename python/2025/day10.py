# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import collections

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_machine_from_line(string):
    lst = string.split(" ")
    diagram, wirings, joltage = lst[0], lst[1:-1], lst[-1]
    diagram = tuple(v == "#" for v in diagram[1:-1])
    wirings = [tuple(int(i) for i in w[1:-1].split(",")) for w in wirings]
    joltage = tuple(int(i) for i in joltage[1:-1].split(","))
    return diagram, wirings, joltage


def get_machines_from_lines(string):
    return [get_machine_from_line(l) for l in string.splitlines()]


def get_machines_from_file(file_path=top_dir + "resources/year2025_day10_input.txt"):
    with open(file_path) as f:
        return get_machines_from_lines(f.read())


def get_nb_button_presses_to_configure(machine, configure_lights):
    diagram, wirings, joltage = machine
    q = collections.deque([(diagram, joltage, [])])
    while q:
        diag, jolt, presses = q.popleft()
        if not any(diag if configure_lights else jolt):
            return len(presses)
        for i, wiring in enumerate(wirings):
            presses2 = presses + [i]
            if configure_lights:
                if all(i > p for p in presses):
                    diag2 = list(diag)
                    for w in wiring:
                        diag2[w] = not diag2[w]
                    q.append((diag2, jolt, presses2))
            else:
                if all(i >= p for p in presses):
                    jolt2 = list(jolt)
                    for w in wiring:
                        jolt2[w] -= 1
                    if all(j >= 0 for j in jolt2):
                        q.append((diag, jolt2, presses2))
    assert False


def get_nb_button_presses_to_configure_all(machines, configure_lights):
    return sum(get_nb_button_presses_to_configure(m, configure_lights) for m in machines)

def run_tests():
    machines = get_machines_from_lines(
        """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    )
    assert get_nb_button_presses_to_configure_all(machines, True) == 7
    assert get_nb_button_presses_to_configure_all(machines, False) == 33


def get_solutions():
    machines = get_machines_from_file()
    print(get_nb_button_presses_to_configure_all(machines, True) == 459)
#    print(get_nb_button_presses_to_configure_all(machines, False)) - TO BE OPTIMISED


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
