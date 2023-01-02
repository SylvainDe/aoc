// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_from_lines;
use common::input::get_answers;
use common::input::get_file_content;
use std::str::FromStr;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day21_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2016_day21_answer.txt";

#[derive(Debug, Eq, Ord, PartialEq, PartialOrd, Clone)]
enum Instruction {
    SwapPosition(usize, usize),
    SwapLetter(char, char),
    RotateRight(usize),
    RotateLeft(usize),
    RotateBasedOnLetter(char),
    ReversePosition(usize, usize),
    MovePosition(usize, usize),
}

type InputContent = Vec<Instruction>;

impl FromStr for Instruction {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let lst = s.split(' ').collect::<Vec<&str>>();
        if let Some(&first) = lst.first() {
            if let Some(&second) = lst.get(1) {
                let get_as_usize = |i: usize| lst[i].parse::<usize>().map_err(|_| {});
                let get_first_char = |i: usize| lst[i].chars().next().ok_or(());
                if first == "swap" {
                    if second == "position" {
                        return Ok(Self::SwapPosition(get_as_usize(2)?, get_as_usize(5)?));
                    } else if second == "letter" {
                        return Ok(Self::SwapLetter(get_first_char(2)?, get_first_char(5)?));
                    }
                } else if first == "rotate" {
                    if second == "left" {
                        return Ok(Self::RotateLeft(get_as_usize(2)?));
                    } else if second == "right" {
                        return Ok(Self::RotateRight(get_as_usize(2)?));
                    } else if second == "based" {
                        return Ok(Self::RotateBasedOnLetter(get_first_char(6)?));
                    }
                } else if first == "reverse" {
                    return Ok(Self::ReversePosition(get_as_usize(2)?, get_as_usize(4)?));
                } else if first == "move" {
                    return Ok(Self::MovePosition(get_as_usize(2)?, get_as_usize(5)?));
                }
            }
        }
        Err(())
    }
}

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

fn apply_instructions(string: &str, instructions: &InputContent) -> String {
    let mut vec = string.chars().collect::<Vec<char>>();
    for ins in instructions {
        match ins {
            Instruction::SwapPosition(pos1, pos2) => vec.swap(*pos1, *pos2),
            Instruction::SwapLetter(c1, c2) => {
                let pos1 = vec.iter().position(|&x| x == *c1).unwrap();
                let pos2 = vec.iter().position(|&x| x == *c2).unwrap();
                vec.swap(pos1, pos2);
            }
            Instruction::RotateRight(pos) => vec.rotate_right(*pos),
            Instruction::RotateLeft(pos) => vec.rotate_left(*pos),
            Instruction::RotateBasedOnLetter(c) => {
                let pos = vec.iter().position(|&x| x == *c).unwrap();
                let rotate = (1 + pos + usize::from(pos >= 4)) % (vec.len());
                vec.rotate_right(rotate);
            }
            Instruction::ReversePosition(pos1, pos2) => {
                assert!(pos1 < pos2);
                let nb_it = (1 + pos2 - pos1) / 2;
                for i in 0..nb_it {
                    vec.swap(pos1 + i, pos2 - i);
                }
            }
            Instruction::MovePosition(pos1, pos2) => {
                let c = vec.remove(*pos1);
                vec.insert(*pos2, c);
            }
        }
    }
    vec.iter().collect()
}

fn revert_instructions(string: &str, instructions: &InputContent) -> String {
    let mut vec = string.chars().collect::<Vec<char>>();
    for ins in instructions.iter().rev() {
        match ins {
            Instruction::SwapPosition(pos1, pos2) => vec.swap(*pos1, *pos2),
            Instruction::SwapLetter(c1, c2) => {
                let pos1 = vec.iter().position(|&x| x == *c1).unwrap();
                let pos2 = vec.iter().position(|&x| x == *c2).unwrap();
                vec.swap(pos1, pos2);
            }
            Instruction::RotateRight(pos) => vec.rotate_left(*pos),
            Instruction::RotateLeft(pos) => vec.rotate_right(*pos),
            Instruction::RotateBasedOnLetter(c) => {
                let pos = vec.iter().position(|&x| x == *c).unwrap();
                // Letter at index p gets moved to either:
                //  - 2p + 1 % L if p < 4
                //  - 2p + 2 % L otherwise
                // which means one of these positions: (2p+1, 2p+2, 2p+1-L, 2p+2-L, 2p+2-2L)
                let len = vec.len();
                let mut done = false;
                for nb_l in 0..=2 {
                    let pos2 = pos + nb_l * len;
                    if pos2 > 0 {
                        let initial_pos = (pos2 - 1) / 2;
                        let rotate = (1 + initial_pos + usize::from(initial_pos >= 4)) % len;
                        if (initial_pos + rotate) % len == pos {
                            assert!(!done);
                            done = true;
                            vec.rotate_left(rotate);
                            break; // Is there a better way to handle ambiguity ?
                        }
                    }
                }
                assert!(done);
            }
            Instruction::ReversePosition(pos1, pos2) => {
                assert!(pos1 < pos2);
                let nb_it = (1 + pos2 - pos1) / 2;
                for i in 0..nb_it {
                    vec.swap(pos1 + i, pos2 - i);
                }
            }
            Instruction::MovePosition(pos1, pos2) => {
                let c = vec.remove(*pos2);
                vec.insert(*pos1, c);
            }
        }
    }
    vec.iter().collect()
}

fn part1(arg: &InputContent) -> String {
    apply_instructions("abcdefgh", arg)
}

fn part2(arg: &InputContent) -> String {
    revert_instructions("fbgdceah", arg)
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(&data);
    check_answer(&res, ans, solved);
    let res2 = part2(&data);
    check_answer(&res2, ans2, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_single_instructions() {
        let tests = vec![
            ("abcde", "ebcda", "swap position 4 with position 0"),
            ("ebcda", "edcba", "swap letter d with letter b"),
            ("edcba", "abcde", "reverse positions 0 through 4"),
            ("abcde", "bcdea", "rotate left 1 step"),
            ("bcdea", "bdeac", "move position 1 to position 4"),
            ("bdeac", "abdec", "move position 3 to position 0"),
            ("abdec", "ecabd", "rotate based on position of letter b"),
            ("ecabd", "decab", "rotate based on position of letter d"),
            // Own tests
            ("bcdea", "abcde", "rotate right 1 step"),
            ("edcbaf", "fabcde", "reverse positions 0 through 5"),
            ("abdec", "decab", "rotate based on position of letter d"),
        ];
        for (begin, end, inst) in tests {
            let i = get_input_from_str(inst);
            assert_eq!(apply_instructions(begin, &i), end);
            if !(begin == "ecabd" && inst == "rotate based on position of letter d") {
                assert_eq!(revert_instructions(end, &i), begin);
            }
        }
    }

    #[test]
    fn test_all_instructions() {
        let inst = "swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d";
        let inst = get_input_from_str(inst);
        assert_eq!(apply_instructions("abcde", &inst), "decab");
        //        assert_eq!(revert_instructions("decab", &inst), "abcde");
    }
}
