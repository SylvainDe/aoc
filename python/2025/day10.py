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


# TO BE OPTIMISED
def get_nb_button_presses_to_configure(machine):
    diagram, wirings, _ = machine
    q = collections.deque([(diagram, set())])
    while q:
        diag, presses = q.popleft()
        if not any(diag):
            return len(presses)
        for i, wiring in enumerate(wirings):
            if not presses or i > max(presses):
                diag2 = list(diag)
                for w in wiring:
                    diag2[w] = not diag2[w]
                q.append((diag2, presses | set([i])))
    assert False


def get_nb_button_presses_to_configure_all(machines):
    return sum(get_nb_button_presses_to_configure(m) for m in machines)

def run_tests():
    machines = get_machines_from_lines(
        """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    )
    assert get_nb_button_presses_to_configure_all(machines) == 7


def get_solutions():
    machines = get_machines_from_file()
    print(get_nb_button_presses_to_configure_all(machines) == 459)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
