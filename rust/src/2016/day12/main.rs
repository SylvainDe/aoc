use common::collect_from_lines;
use common::get_file_content;
use core::str::FromStr;
use std::collections::HashMap;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day12_input.txt";

type Int = i32;

#[derive(Debug, Eq, Ord, PartialEq, PartialOrd)]
enum Instruction {
    Copy(String, String),
    Increase(String),
    Decrease(String),
    Jump(String, String),
}

impl FromStr for Instruction {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let chunks: Vec<&str> = s.split(' ').collect();
        match chunks.first() {
            None => (),
            Some(&cmd) => match cmd {
                "inc" => {
                    if chunks.len() == 2 {
                        return Ok(Self::Increase((*chunks.get(1).unwrap()).to_string()));
                    }
                }
                "dec" => {
                    if chunks.len() == 2 {
                        return Ok(Self::Decrease((*chunks.get(1).unwrap()).to_string()));
                    }
                }
                "cpy" => {
                    if chunks.len() == 3 {
                        return Ok(Self::Copy(
                            (*chunks.get(1).unwrap()).to_string(),
                            (*chunks.get(2).unwrap()).to_string(),
                        ));
                    }
                }
                "jnz" => {
                    if chunks.len() == 3 {
                        return Ok(Self::Jump(
                            (*chunks.get(1).unwrap()).to_string(),
                            (*chunks.get(2).unwrap()).to_string(),
                        ));
                    }
                }
                _ => (),
            },
        }
        Err(())
    }
}

type InputContent = Vec<Instruction>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string, Instruction::from_str)
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&get_file_content(filepath))
}

#[allow(clippy::cast_sign_loss)]
fn run_instructions(instructions: &InputContent, c_value: Int) -> Int {
    let mut env = HashMap::from([
        ("a".to_string(), 0),
        ("b".to_string(), 0),
        ("c".to_string(), c_value),
        ("d".to_string(), 0),
    ]);
    let mut cnt = 0;
    while let Some(ins) = instructions.get(cnt as usize) {
        match ins {
            Instruction::Copy(x, y) => {
                let val = match x.parse::<Int>() {
                    Ok(n) => n,
                    Err(_) => *env.get(x).unwrap(),
                };
                env.insert(y.to_string(), val);
            }
            Instruction::Increase(x) => {
                env.entry(x.to_string()).and_modify(|e| *e += 1);
            }
            Instruction::Decrease(x) => {
                env.entry(x.to_string()).and_modify(|e| *e -= 1);
            }
            Instruction::Jump(x, y) => {
                let x = match x.parse::<Int>() {
                    Ok(n) => n,
                    Err(_) => *env.get(x).unwrap(),
                };
                if x != 0 {
                    let rel_pos = y.parse::<Int>().unwrap();
                    cnt += rel_pos;
                    continue;
                }
            }
        }
        cnt += 1;
    }
    *env.get("a").unwrap()
}

fn part1(instructions: &InputContent) -> Int {
    run_instructions(instructions, 0)
}

fn part2(instructions: &InputContent) -> Int {
    run_instructions(instructions, 1)
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 318_083);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 9_227_737);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a";

    #[test]
    fn test_instruction_from_str() {
        assert_eq!(
            Instruction::from_str("cpy 41 a"),
            Ok(Instruction::Copy("41".to_string(), "a".to_string()))
        );
        assert_eq!(
            Instruction::from_str("jnz a 2"),
            Ok(Instruction::Jump("a".to_string(), "2".to_string()))
        );
        assert_eq!(
            Instruction::from_str("inc a"),
            Ok(Instruction::Increase("a".to_string()))
        );
        assert_eq!(
            Instruction::from_str("dec a"),
            Ok(Instruction::Decrease("a".to_string()))
        );
        assert!(Instruction::from_str("").is_err());
        assert!(Instruction::from_str("abc").is_err());
        assert!(Instruction::from_str("cpy").is_err());
        assert!(Instruction::from_str("cpy 41").is_err());
        assert!(Instruction::from_str("cpy 41 a b").is_err());
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 42);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 42);
    }
}
