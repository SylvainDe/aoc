use common::input::get_first_line_from_file;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2017_day9_input.txt";

type Int = u32;

fn get_input_from_str(string: &str) -> String {
    string.to_string()
}

fn get_input_from_file(filepath: &str) -> String {
    get_input_from_str(&get_first_line_from_file(filepath))
}

fn parse_str(string: &str) -> (Int, Int) {
    #[derive(Debug, PartialEq)]
    enum State {
        Normal,
        Garbage,
        GarbageSkipNext,
    }
    let mut state = State::Normal;
    let mut depth = 0;
    let mut removed = 0;
    let mut score = 0;
    for c in string.chars() {
        match state {
            State::Normal => match c {
                '{' => {
                    depth += 1;
                    score += depth;
                }
                '}' => depth -= 1,
                '<' => state = State::Garbage,
                _ => (),
            },
            State::Garbage => match c {
                '>' => state = State::Normal,
                '!' => state = State::GarbageSkipNext,
                _ => removed += 1,
            },
            State::GarbageSkipNext => state = State::Garbage,
        }
    }
    assert_eq!(state, State::Normal);
    assert_eq!(depth, 0);
    (score, removed)
}

fn part1(string: &str) -> Int {
    let (score, _) = parse_str(string);
    score
}

fn part2(string: &str) -> Int {
    let (_, removed) = parse_str(string);
    removed
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 16869);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 7284);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "";

    #[test]
    fn test_part1() {
        // Self-contained garbage
        assert_eq!(parse_str("<>"), (0, 0));
        assert_eq!(parse_str("<random characters>"), (0, 17));
        assert_eq!(parse_str("<<<<>"), (0, 3));
        assert_eq!(parse_str("<{!>}>"), (0, 2));
        assert_eq!(parse_str("<!!>"), (0, 0));
        assert_eq!(parse_str("<!!!>>"), (0, 0));
        assert_eq!(parse_str("<{o\"i!a,<{i<a>"), (0, 10));
        // Whole stream
        assert_eq!(part1("{}"), 1);
        assert_eq!(part1("{{{}}}"), 6);
        assert_eq!(part1("{{},{}}"), 5);
        assert_eq!(part1("{{{},{},{{}}}}"), 16);
        assert_eq!(part1("{<a>,<a>,<a>,<a>}"), 1);
        assert_eq!(part1("{{<ab>},{<ab>},{<ab>},{<ab>}}"), 9);
        assert_eq!(part1("{{<!!>},{<!!>},{<!!>},{<!!>}}"), 9);
        assert_eq!(part1("{{<a!>},{<a!>},{<a!>},{<ab>}}"), 3);
        assert_eq!(part1(""), 0);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
