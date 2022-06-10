use common::get_first_line;
use std::collections::HashSet;
use std::fs;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2015_day3_input.txt";

type InputContent = String;

fn get_input_from_str(string: &str) -> InputContent {
    get_first_line(string)
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

type Position = (i32, i32);

fn get_path(input: impl Iterator<Item = char>) -> HashSet<Position> {
    let mut x: i32 = 0;
    let mut y: i32 = 0;
    let mut pos = HashSet::<(i32, i32)>::new();
    pos.insert((x, y));
    for c in input {
        match c {
            '^' => x += 1,
            'v' => x -= 1,
            '<' => y -= 1,
            '>' => y += 1,
            _ => panic!("Unexpected value {}", c),
        }
        pos.insert((x, y));
    }
    pos
}

fn part1(input: &InputContent) -> usize {
    get_path(input.chars()).len()
}

fn part2(input: &InputContent) -> usize {
    let mut path1 = get_path(input.chars().step_by(2));
    let mut char_it = input.chars();
    char_it.next();
    path1.extend(get_path(char_it.step_by(2)));
    path1.len()
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 2081);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 2341);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str("")), 1);
        assert_eq!(part1(&get_input_from_str(">")), 2);
        assert_eq!(part1(&get_input_from_str("^>v<")), 4);
        assert_eq!(part1(&get_input_from_str("^v^v^v^v^v")), 2);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str("")), 1);
        assert_eq!(part2(&get_input_from_str("^v")), 3);
        assert_eq!(part2(&get_input_from_str("^>v<")), 3);
        assert_eq!(part2(&get_input_from_str("^v^v^v^v^v")), 11);
    }
}
