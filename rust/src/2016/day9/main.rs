use common::get_file_content;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day9_input.txt";

type Int = u32;

fn get_input_from_file(filepath: &str) -> String {
    get_file_content(filepath)
}

fn part1(s: &str) -> Int {
    // Implement a state machine to avoid performing string manipulation
    #[derive(Debug, PartialEq)]
    enum State {
        Normal,
        InNbChars,
        InNbRepetition,
    }
    let mut state = State::Normal;
    let mut it = s.chars();
    let mut nb_char = 0;
    let mut nb_rep = 0;
    let mut len = 0;
    while let Some(c) = it.next() {
        match state {
            State::Normal => match c {
                '(' => state = State::InNbChars,
                '\n' => (),
                _ => len += 1,
            },
            State::InNbChars => match c {
                'x' => state = State::InNbRepetition,
                '0'..='9' => nb_char = 10 * nb_char + (c as u32 - '0' as u32),
                _ => panic!("Unexpected char {} in state {:?}", c, state),
            },
            State::InNbRepetition => match c {
                ')' => {
                    state = State::Normal;
                    for _ in 0..nb_char {
                        let res = it.next();
                        assert!(res.is_some());
                    }
                    len += nb_char * nb_rep;
                    nb_char = 0;
                    nb_rep = 0;
                }
                '0'..='9' => nb_rep = 10 * nb_rep + (c as u32 - '0' as u32),
                _ => panic!("Unexpected char {} in state {:?}", c, state),
            },
        }
    }
    assert_eq!(state, State::Normal);
    len
}

#[allow(clippy::missing_const_for_fn)]
fn part2(_arg: &str) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 99145);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "";

    #[test]
    fn test_part1() {
        assert_eq!(part1("ADVENT"), 6);
        assert_eq!(part1("A(1x5)BC"), 7);
        assert_eq!(part1("(3x3)XYZ"), 9);
        assert_eq!(part1("A(2x2)BCD(2x2)EFG"), 11);
        assert_eq!(part1("(6x1)(1x3)A"), 6);
        assert_eq!(part1("X(8x2)(3x3)ABCY"), 18);
        assert_eq!(part1("ADVENT\n"), 6);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(EXAMPLE), 0);
    }
}
