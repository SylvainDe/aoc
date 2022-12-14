use common::input::collect_from_lines;
use common::input::get_file_content;
use std::collections::HashMap;
use std::str::FromStr;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2021_day24_input.txt";

type Int = i64;

#[derive(Debug, Eq, Ord, PartialEq, PartialOrd, Clone)]
enum Instruction {
    Input(String),
    BinaryOp(String, String, fn(Int, Int) -> Int),
}

type InputContent = Vec<Instruction>;

impl FromStr for Instruction {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let chunks: Vec<&str> = s.split(' ').collect();
        match chunks.first() {
            None => (),
            Some(&cmd) => match chunks.len() {
                2 => {
                    let arg1 = chunks[1].to_owned();
                    if cmd == "inp" {
                        return Ok(Self::Input(arg1));
                    }
                }
                3 => {
                    let arg1 = chunks[1].to_owned();
                    let arg2 = chunks[2].to_owned();
                    match cmd {
                        "add" => {
                            return Ok(Self::BinaryOp(arg1, arg2, |a1, a2| a1 + a2));
                        }
                        "mul" => {
                            return Ok(Self::BinaryOp(arg1, arg2, |a1, a2| a1 * a2));
                        }
                        "div" => {
                            return Ok(Self::BinaryOp(arg1, arg2, |a1, a2| a1 / a2));
                        }
                        "mod" => {
                            return Ok(Self::BinaryOp(arg1, arg2, |a1, a2| a1 % a2));
                        }
                        "eql" => {
                            return Ok(Self::BinaryOp(
                                arg1,
                                arg2,
                                |a1, a2| if a1 == a2 { 1 } else { 0 },
                            ));
                        }
                        _ => (),
                    }
                }
                _ => (),
            },
        }
        Err(())
    }
}

#[allow(dead_code)]
fn eval_string(s: &str, env: &HashMap<String, Int>) -> Int {
    match s.parse::<Int>() {
        Ok(n) => n,
        Err(_) => *env.get(s).unwrap(),
    }
}

#[allow(dead_code)]
fn run_instructions_on_nb(instructions: &InputContent, input: u64) -> (Int, Int, Int, Int) {
    if input == 0 {
        return run_instructions(instructions, &[0]);
    }
    //dbg!(&input);
    let mut input = input;
    let mut digits: Vec<Int> = Vec::new();
    while input > 0 {
        digits.push((input % 10).try_into().unwrap());
        input /= 10;
    }
    digits.reverse();
    //dbg!(&digits);
    run_instructions(instructions, &digits)
}

fn run_instructions(instructions: &InputContent, input: &[Int]) -> (Int, Int, Int, Int) {
    let mut env: HashMap<String, Int> = HashMap::from([
        ("w".to_owned(), 0),
        ("x".to_owned(), 0),
        ("y".to_owned(), 0),
        ("z".to_owned(), 0),
    ]);
    let mut input_iter = input.iter();
    for ins in instructions {
        match ins {
            Instruction::Input(s1) => {
                env.insert(s1.clone(), *input_iter.next().unwrap());
            }
            Instruction::BinaryOp(s1, s2, f) => {
                let res = f(eval_string(s1, &env), eval_string(s2, &env));
                env.insert(s1.clone(), res);
            }
        }
    }
    (env["w"], env["x"], env["y"], env["z"])
}

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

#[allow(clippy::missing_const_for_fn)]
fn part1(_instructions: &InputContent) -> Int {
    // This may actually be an exercice of reverse engineering
    0
}

#[allow(clippy::missing_const_for_fn)]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 0);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE1: &str = "inp x
mul x -1";
    const EXAMPLE2: &str = "inp z
inp x
mul z 3
eql z x";
    const EXAMPLE3: &str = "inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2";

    #[test]
    fn test_instruction_from_str() {
        get_input_from_str(EXAMPLE1);
        get_input_from_str(EXAMPLE2);
        get_input_from_str(EXAMPLE3);
    }

    #[test]
    fn test_run_instructions() {
        let input1 = get_input_from_str(EXAMPLE1);
        assert_eq!(run_instructions(&input1, &[3]), (0, -3, 0, 0));
        assert_eq!(run_instructions_on_nb(&input1, 3), (0, -3, 0, 0));
        let input2 = get_input_from_str(EXAMPLE2);
        assert_eq!(run_instructions(&input2, &[3, 9]), (0, 9, 0, 1));
        assert_eq!(run_instructions_on_nb(&input2, 39), (0, 9, 0, 1));
        assert_eq!(run_instructions(&input2, &[3, 8]), (0, 8, 0, 0));
        assert_eq!(run_instructions_on_nb(&input2, 38), (0, 8, 0, 0));
        let input3 = get_input_from_str(EXAMPLE3);
        assert_eq!(run_instructions(&input3, &[7]), (0, 1, 1, 1));
        assert_eq!(run_instructions_on_nb(&input3, 7), (0, 1, 1, 1));
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE1)), 0);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE2)), 0);
    }
}
