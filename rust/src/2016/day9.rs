use common::input::get_first_line_from_file;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day9_input.txt";

// Implement a state machine to avoid performing string manipulation
#[derive(Debug, PartialEq)]
enum State {
    Normal,
    InNbChars,
    InNbRepetition,
}

fn part1(s: &str) -> u32 {
    let mut state = State::Normal;
    let mut it = s.chars();
    let mut nb_char = 0;
    let mut nb_rep = 0;
    let mut len = 0;
    while let Some(c) = it.next() {
        match state {
            State::Normal => match c {
                '(' => state = State::InNbChars,
                _ => len += 1,
            },
            State::InNbChars => match c {
                'x' => state = State::InNbRepetition,
                '0'..='9' => nb_char = 10 * nb_char + (c as u32 - '0' as u32),
                _ => panic!("Unexpected char {} in state {:?}", c, state),
            },
            State::InNbRepetition => match c {
                ')' => {
                    for _ in 0..nb_char {
                        let res = it.next();
                        assert!(res.is_some());
                    }
                    len += nb_char * nb_rep;
                    state = State::Normal;
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

fn part2(s: &str) -> u64 {
    let mut state = State::Normal;
    let mut nb_char = 0;
    let mut nb_rep = 0;
    let mut len = 0;
    for (i, c) in s.chars().enumerate() {
        match state {
            State::Normal => match c {
                '(' => state = State::InNbChars,
                _ => len += 1,
            },
            State::InNbChars => match c {
                'x' => state = State::InNbRepetition,
                '0'..='9' => nb_char = 10 * nb_char + (c as usize - '0' as usize),
                _ => panic!("Unexpected char {} in state {:?}", c, state),
            },
            State::InNbRepetition => match c {
                ')' => {
                    assert!(nb_rep > 0);
                    len += (nb_rep - 1) * part2(&s[i + 1..i + 1 + nb_char]);
                    state = State::Normal;
                    nb_char = 0;
                    nb_rep = 0;
                }
                '0'..='9' => nb_rep = 10 * nb_rep + (c as u64 - '0' as u64),
                _ => panic!("Unexpected char {} in state {:?}", c, state),
            },
        }
    }
    assert_eq!(state, State::Normal);
    len
}

fn main() {
    let before = Instant::now();
    let data = get_first_line_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 99145);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 10_943_094_568);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1("ADVENT"), 6);
        assert_eq!(part1("A(1x5)BC"), 7);
        assert_eq!(part1("(3x3)XYZ"), 9);
        assert_eq!(part1("A(2x2)BCD(2x2)EFG"), 11);
        assert_eq!(part1("(6x1)(1x3)A"), 6);
        assert_eq!(part1("X(8x2)(3x3)ABCY"), 18);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2("(3x3)XYZ"), 9);
        assert_eq!(part2("X(8x2)(3x3)ABCY"), 20);
        assert_eq!(part2("(27x12)(20x12)(13x14)(7x10)(1x12)A"), 241_920);
        assert_eq!(
            part2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"),
            445
        );
    }
}
