# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import itertools
import math

top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"


def get_box_from_line(string):
    return tuple(int(s) for s in string.split(","))


def get_boxes_from_lines(string):
    return [get_box_from_line(l) for l in string.splitlines()]


def get_boxes_from_file(file_path=top_dir + "resources/year2025_day8_input.txt"):
    with open(file_path) as f:
        return get_boxes_from_lines(f.read())

def dist_squared(b1, b2):
    deltas = (c1 - c2 for c1, c2 in zip(b1, b2))
    return sum(d*d for d in deltas)

def get_circuit_with_box(circuits, box):
    ret = None
    for c in circuits:
        if box in c:
            assert ret is None
            ret = c
    assert ret is not None
    return ret

def get_circuits(boxes, nb_conn):
   circuits = [set([b]) for b in boxes]
   pairs = sorted(list(itertools.combinations(boxes, 2)), key=lambda boxes: dist_squared(*boxes))
   for _, (b1, b2) in zip(range(nb_conn), pairs):
       b1_circuit = get_circuit_with_box(circuits, b1)
       b2_circuit = get_circuit_with_box(circuits, b2)
       if b1_circuit != b2_circuit:
           circuits.remove(b1_circuit)
           b2_circuit.update(b1_circuit)
   return math.prod(sorted((len(c) for c in circuits), reverse=True)[:3])


def get_last_junction(boxes):
   circuits = [set([b]) for b in boxes]
   pairs = sorted(list(itertools.combinations(boxes, 2)), key=lambda boxes: dist_squared(*boxes))
   for (b1, b2) in pairs:
       b1_circuit = get_circuit_with_box(circuits, b1)
       b2_circuit = get_circuit_with_box(circuits, b2)
       if b1_circuit != b2_circuit:
           circuits.remove(b1_circuit)
           b2_circuit.update(b1_circuit)
           if len(circuits) == 1:
               return b1[0] * b2[0]


def run_tests():
    boxes = get_boxes_from_lines(
        """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
    )
    assert get_circuits(boxes, 10) == 40
    assert get_last_junction(boxes) == 25272


def get_solutions():
    boxes = get_boxes_from_file()
    print(get_circuits(boxes, 1000) == 131580)
    print(get_last_junction(boxes) == 6844224)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
