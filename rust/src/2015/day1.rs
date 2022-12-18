// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_first_line_from_file;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2015_day1_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2015_day1_answer.txt";

fn floor_value(c: char) -> i32 {
    match c {
        '(' => 1,
        ')' => -1,
        _ => panic!("Unexpected value {}", c),
    }
}

fn part1(string: &str) -> i32 {
    string.chars().map(floor_value).sum()
}

fn part2(string: &str) -> usize {
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
    let data = get_first_line_from_file(INPUT_FILEPATH);
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(&data);
    check_answer(&res.to_string(), ans, solved);
    let res2 = part2(&data);
    check_answer(&res2.to_string(), ans2, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1("(())"), 0);
        assert_eq!(part1("()()"), 0);
        assert_eq!(part1("((("), 3);
        assert_eq!(part1("(()(()("), 3);
        assert_eq!(part1("))((((("), 3);
        assert_eq!(part1("())"), -1);
        assert_eq!(part1("))("), -1);
        assert_eq!(part1(")))"), -3);
        assert_eq!(part1(")())())"), -3);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(")"), 1);
        assert_eq!(part2("()())"), 5);
    }
}
