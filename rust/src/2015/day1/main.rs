use common::get_first_line;
use std::fs;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2015_day1_input.txt";

type InputContent = String;

fn get_input_from_str(string: &str) -> InputContent {
    get_first_line(string)
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

fn floor_value(c: char) -> i32 {
    match c {
        '(' => 1,
        ')' => -1,
        _ => panic!("Unexpected value {}", c),
    }
}

fn part1(string: &InputContent) -> i32 {
    string.chars().map(floor_value).sum()
}

fn part2(string: &InputContent) -> usize {
    let mut floor = 0;
    for (i, f) in string.chars().map(floor_value).enumerate() {
        floor += f;
        if floor == -1 {
            return i + 1;
        }
    }
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 232);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 1783);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str("(())")), 0);
        assert_eq!(part1(&get_input_from_str("()()")), 0);
        assert_eq!(part1(&get_input_from_str("(((")), 3);
        assert_eq!(part1(&get_input_from_str("(()(()(")), 3);
        assert_eq!(part1(&get_input_from_str("))(((((")), 3);
        assert_eq!(part1(&get_input_from_str("())")), -1);
        assert_eq!(part1(&get_input_from_str("))(")), -1);
        assert_eq!(part1(&get_input_from_str(")))")), -3);
        assert_eq!(part1(&get_input_from_str(")())())")), -3);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(")")), 1);
        assert_eq!(part2(&get_input_from_str("()())")), 5);
    }
}
