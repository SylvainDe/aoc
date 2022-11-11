use common::collect_from_lines;
use common::get_file_content;
use core::str::FromStr;
use std::collections::HashMap;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day23_input.txt";

type Int = i32;
const SKIP_SLOW: bool = true;

// TODO: Put in common with assembunny logic for day 12
#[derive(Debug, Eq, Ord, PartialEq, PartialOrd, Clone)]
enum Instruction {
    Copy(String, String),
    Increase(String),
    Decrease(String),
    Jump(String, String),
    Toggle(String),
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
                "tgl" => {
                    if chunks.len() == 2 {
                        return Ok(Self::Toggle((*chunks.get(1).unwrap()).to_string()));
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

#[allow(clippy::missing_const_for_fn)]
fn toggle_ins(ins: Instruction) -> Instruction {
    match ins {
        // For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc
        Instruction::Increase(x) => Instruction::Decrease(x),
        Instruction::Decrease(x) | Instruction::Toggle(x) => Instruction::Increase(x),
        // For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz
        Instruction::Jump(x, y) => Instruction::Copy(x, y),
        Instruction::Copy(x, y) => Instruction::Jump(x, y),
    }
}

fn eval_string(s: &str, env: &HashMap<String, Int>) -> Int {
    match s.parse::<Int>() {
        Ok(n) => n,
        Err(_) => *env.get(s).unwrap(),
    }
}

#[allow(clippy::cast_sign_loss)]
fn run_instructions(instructions: &InputContent, a_value: Int, c_value: Int) -> Int {
    let mut instructions = instructions.clone();
    let mut env = HashMap::from([
        ("a".to_string(), a_value),
        ("b".to_string(), 0),
        ("c".to_string(), c_value),
        ("d".to_string(), 0),
    ]);
    let mut cnt = 0;
    while let Some(ins) = instructions.get(cnt as usize) {
        match ins {
            Instruction::Copy(x, y) => {
                let x = eval_string(x, &env);
                env.insert(y.to_string(), x);
            }
            Instruction::Increase(x) => {
                env.entry(x.to_string()).and_modify(|e| *e += 1);
            }
            Instruction::Decrease(x) => {
                env.entry(x.to_string()).and_modify(|e| *e -= 1);
            }
            Instruction::Toggle(x) => {
                let x = eval_string(x, &env);
                let pos = (cnt + x) as usize;
                if let Some(ins2) = instructions.get(pos) {
                    instructions[pos] = toggle_ins(ins2.clone());
                }
            }
            Instruction::Jump(x, y) => {
                let x = eval_string(x, &env);
                if x != 0 {
                    let y = eval_string(y, &env);
                    cnt += y;
                    continue;
                }
            }
        }
        cnt += 1;
    }
    *env.get("a").unwrap()
}

fn part1(instructions: &InputContent) -> Int {
    run_instructions(instructions, 7, 0)
}

fn part2(instructions: &InputContent) -> Int {
    run_instructions(instructions, 12, 0)
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 13958);
    if !SKIP_SLOW {
        // TODO: This is very slow. The original asm code needs to be
        // optimised, probably with the introduction of new instructions
        // such as multiply
        let res2 = part2(&data);
        println!("{:?}", res2);
        assert_eq!(res2, 479_010_518); // Obtained in 2100 secs
    }
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DAY_12: &str = "cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a";

    const EXAMPLE_DAY_23: &str = "cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
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
        assert_eq!(
            Instruction::from_str("tgl a"),
            Ok(Instruction::Toggle("a".to_string()))
        );
        assert!(Instruction::from_str("").is_err());
        assert!(Instruction::from_str("abc").is_err());
        assert!(Instruction::from_str("cpy").is_err());
        assert!(Instruction::from_str("cpy 41").is_err());
        assert!(Instruction::from_str("cpy 41 a b").is_err());
    }

    #[test]
    fn test_day12() {
        assert_eq!(
            run_instructions(&get_input_from_str(EXAMPLE_DAY_12), 0, 0),
            42
        );
        assert_eq!(
            run_instructions(&get_input_from_str(EXAMPLE_DAY_12), 0, 1),
            42
        );
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE_DAY_23)), 3);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE_DAY_23)), 3);
    }
}
