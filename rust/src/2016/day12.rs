// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::assembunny2016::run_instructions;
use common::assembunny2016::Instruction;
use common::input::collect_from_lines;
use common::input::get_file_content;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day12_input.txt";

type Int = i32;

type InputContent = Vec<Instruction>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

fn part1(instructions: &InputContent) -> Int {
    run_instructions(instructions, 0, 0)
}

fn part2(instructions: &InputContent) -> Int {
    run_instructions(instructions, 0, 1)
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
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
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 42);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 42);
    }
}
