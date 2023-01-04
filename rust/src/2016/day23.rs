// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::assembunny2016::get_input_from_str;
use common::assembunny2016::run_instructions;
use common::assembunny2016::Instructions;
use common::assembunny2016::Int;
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_file_content;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day23_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2016_day23_answer.txt";

const SKIP_SLOW: bool = true;

fn part1(instructions: &Instructions) -> Int {
    run_instructions(instructions, 7, 0)
}

fn part2(instructions: &Instructions) -> Int {
    run_instructions(instructions, 12, 0)
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(&data);
    check_answer(&res.to_string(), ans, solved);
    if !SKIP_SLOW {
        // TODO: This is very slow. The original asm code needs to be
        // optimised, probably with the introduction of new instructions
        // such as multiply
        let res2 = part2(&data);
        check_answer(&res2.to_string(), ans2, solved); // Obtained in 2100 secs
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
