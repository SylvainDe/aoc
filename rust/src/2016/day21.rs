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
    ReversePositions(usize, usize),
    MovePosition(usize, usize),
    RotateRight(usize),
    RotateLeft(usize),
    RotateBasedOnLetter(char),
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
                } else if first == "reverse" {
                    return Ok(Self::ReversePositions(get_as_usize(2)?, get_as_usize(4)?));
                } else if first == "move" {
                    return Ok(Self::MovePosition(get_as_usize(2)?, get_as_usize(5)?));
                } else if first == "rotate" {
                    if second == "left" {
                        return Ok(Self::RotateLeft(get_as_usize(2)?));
                    } else if second == "right" {
                        return Ok(Self::RotateRight(get_as_usize(2)?));
                    } else if second == "based" {
                        return Ok(Self::RotateBasedOnLetter(get_first_char(6)?));
                    }
                }
            }
        }
        Err(())
    }
}

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

fn get_pos(vec: &[char], c: char) -> Option<usize> {
    vec.iter().position(|&x| x == c)
}

fn swap_positions_copy(vec: &[char], pos1: usize, pos2: usize) -> Vec<char> {
    let mut vec2 = vec.to_owned();
    vec2.swap(pos1, pos2);
    vec2
}

fn swap_letters(vec: &mut [char], c1: char, c2: char) {
    let pos1 = get_pos(vec, c1).unwrap();
    let pos2 = get_pos(vec, c2).unwrap();
    vec.swap(pos1, pos2);
}

fn swap_letters_copy(vec: &[char], c1: char, c2: char) -> Vec<char> {
    let mut vec2 = vec.to_owned();
    swap_letters(&mut vec2, c1, c2);
    vec2
}

fn rotate_copy(vec: &[char], pos: usize, right: bool) -> Vec<char> {
    let pos = pos % vec.len();
    let mut vec2 = vec.to_owned();
    if right {
        vec2.rotate_right(pos);
    } else {
        vec2.rotate_left(pos);
    }
    vec2
}

fn move_position(vec: &mut Vec<char>, pos1: usize, pos2: usize) {
    let c = vec.remove(pos1);
    vec.insert(pos2, c);
}

fn move_position_copy(vec: &[char], pos1: usize, pos2: usize) -> Vec<char> {
    let mut vec2 = vec.to_owned();
    move_position(&mut vec2, pos1, pos2);
    vec2
}

fn reverse_positions(vec: &mut [char], pos1: usize, pos2: usize) {
    assert!(pos1 < pos2);
    let nb_it = (1 + pos2 - pos1) / 2;
    for i in 0..nb_it {
        vec.swap(pos1 + i, pos2 - i);
    }
}

fn reverse_positions_copy(vec: &[char], pos1: usize, pos2: usize) -> Vec<char> {
    let mut vec2 = vec.to_owned();
    reverse_positions(&mut vec2, pos1, pos2);
    vec2
}

fn vec2str(vec: &[char]) -> String {
    vec.iter().collect()
}

fn apply_instruction(vec: &[char], instruction: &Instruction) -> Vec<char> {
    match instruction {
        Instruction::SwapPosition(pos1, pos2) => swap_positions_copy(vec, *pos1, *pos2),
        Instruction::SwapLetter(c1, c2) => swap_letters_copy(vec, *c1, *c2),
        Instruction::ReversePositions(pos1, pos2) => reverse_positions_copy(vec, *pos1, *pos2),
        Instruction::MovePosition(pos1, pos2) => move_position_copy(vec, *pos1, *pos2),
        Instruction::RotateRight(pos) => rotate_copy(vec, *pos, true),
        Instruction::RotateLeft(pos) => rotate_copy(vec, *pos, false),
        Instruction::RotateBasedOnLetter(c) => {
            let pos = get_pos(vec, *c).unwrap();
            let rotate = 1 + pos + usize::from(pos >= 4);
            rotate_copy(vec, rotate, true)
        }
    }
}

fn revert_instruction(vec: &[char], instruction: &Instruction) -> Vec<Vec<char>> {
    let mut ret = Vec::new();
    match instruction {
        Instruction::SwapPosition(pos1, pos2) => ret.push(swap_positions_copy(vec, *pos1, *pos2)),
        Instruction::SwapLetter(c1, c2) => ret.push(swap_letters_copy(vec, *c1, *c2)),
        Instruction::ReversePositions(p1, p2) => ret.push(reverse_positions_copy(vec, *p1, *p2)),
        Instruction::MovePosition(pos1, pos2) => ret.push(move_position_copy(vec, *pos2, *pos1)),
        Instruction::RotateRight(pos) => ret.push(rotate_copy(vec, *pos, false)),
        Instruction::RotateLeft(pos) => ret.push(rotate_copy(vec, *pos, true)),
        Instruction::RotateBasedOnLetter(c) => {
            let pos = get_pos(vec, *c).unwrap();
            // Letter at index p gets moved to either:
            //  - 2p + 1 % L if p < 4
            //  - 2p + 2 % L otherwise
            // which means one of these positions: (2p+1, 2p+2, 2p+1-L, 2p+2-L, 2p+2-2L)
            // In the other directions, if letter is at index q, we could come from:
            //  - (q - 1) // 2
            //  - (q - 2) // 2
            //  - (q + L - 1) // 2
            //  - (q + L - 2) // 2
            //  - (q + 2L - 2) // 2
            let len = vec.len();
            for nb_l in 0..=2 {
                let pos2 = pos + nb_l * len;
                let shift = if pos2 % 2 == 0 { 2 } else { 1 };
                if pos2 >= shift {
                    assert!((pos2 - shift) % 2 == 0);
                    let initial_pos = (pos2 - shift) / 2;
                    if initial_pos < len {
                        let rotate = 1 + initial_pos + usize::from(initial_pos >= 4);
                        if (initial_pos + rotate) % len == pos {
                            ret.push(rotate_copy(vec, rotate, false));
                        }
                    }
                }
            }
        }
    }
    assert!(!ret.is_empty());
    for v in &ret {
        assert_eq!(vec, apply_instruction(v, instruction));
    }
    ret
}

fn apply_instructions(string: &str, instructions: &InputContent) -> String {
    let mut vec = string.chars().collect::<Vec<char>>();
    for ins in instructions {
        vec = apply_instruction(&vec, ins);
    }
    vec2str(&vec)
}

fn revert_instructions(string: &str, instructions: &InputContent) -> Vec<String> {
    let mut vec = vec![string.chars().collect::<Vec<char>>()];
    for ins in instructions.iter().rev() {
        let mut vec2 = Vec::new();
        for v in vec {
            for v2 in revert_instruction(&v, ins) {
                vec2.push(v2);
            }
        }
        vec = vec2;
    }
    vec.iter().map(|v| vec2str(v)).collect()
}

fn part1(arg: &InputContent) -> String {
    apply_instructions("abcdefgh", arg)
}

fn part2(arg: &InputContent) -> String {
    let v = revert_instructions("fbgdceah", arg);
    assert_eq!(v.len(), 1);
    v[0].clone()
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
            assert!(revert_instructions(end, &i).contains(&begin.to_owned()));
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
        assert!(revert_instructions("decab", &inst).contains(&"abcde".to_owned()));
    }
}
