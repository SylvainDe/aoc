use common::assembunny2016::run_instructions;
use common::assembunny2016::Instruction;
use common::input::collect_from_lines;
use common::input::get_file_content;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day23_input.txt";

const SKIP_SLOW: bool = true;
type Int = i32;

type InputContent = Vec<Instruction>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&get_file_content(filepath))
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

    const EXAMPLE_DAY_23: &str = "cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE_DAY_23)), 3);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE_DAY_23)), 3);
    }
}
