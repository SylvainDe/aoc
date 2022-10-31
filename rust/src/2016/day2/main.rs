use common::collect_lines;
use common::get_file_content;
use std::collections::HashMap;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day2_input.txt";

type InputContent = Vec<String>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_lines(string)
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&get_file_content(filepath))
}

type Keypad = Vec<String>;
type KeypadGraph = HashMap<(char /*Position*/, char /*Direction*/), char /*New position*/>;

fn build_keypad_graph(keypad: &Keypad) -> KeypadGraph {
    let mut graph = KeypadGraph::new();
    for s in keypad.iter() {
        for (a, b) in s.chars().zip(s.chars().skip(1)) {
            if a != ' ' && b != ' ' {
                graph.insert((a, 'R'), b);
                graph.insert((b, 'L'), a);
            }
        }
    }
    for (s1, s2) in keypad.iter().zip(keypad.iter().skip(1)) {
        for (a, b) in s1.chars().zip(s2.chars()) {
            if a != ' ' && b != ' ' {
                graph.insert((a, 'D'), b);
                graph.insert((b, 'U'), a);
            }
        }
    }
    graph
}

fn get_code(keypad: &Keypad, instructions: &InputContent) -> String {
    let g = build_keypad_graph(keypad);
    let mut pos = '5';
    let mut positions = Vec::<char>::new();
    for instruction in instructions.iter() {
        for c in instruction.chars() {
            if let Some(new_position) = g.get(&(pos, c)) {
                pos = *new_position;
            }
        }
        positions.push(pos);
    }
    positions.iter().collect()
}

fn part1(instructions: &InputContent) -> String {
    let keypad = collect_lines(
        "
123
456
789",
    );
    get_code(&keypad, instructions)
}

fn part2(instructions: &InputContent) -> String {
    let keypad = collect_lines(
        "
  1
 234
56789
 ABC
  D ",
    );
    get_code(&keypad, instructions)
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, "53255");
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, "7423A");
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "ULL
RRDDD
LURDL
UUUUD";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), "1985");
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), "5DB3");
    }
}
