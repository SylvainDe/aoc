// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::assembunny2016::get_input_from_str;
use common::assembunny2016::run_instructions;
use common::assembunny2016::Instructions;
use common::assembunny2016::Int;
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_file_content;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day12_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2016_day12_answer.txt";

fn part1(instructions: &Instructions) -> Int {
    run_instructions(instructions, 0, 0)
}

fn part2(instructions: &Instructions) -> Int {
    run_instructions(instructions, 0, 1)
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(&data);
    check_answer(&res.to_string(), ans, solved);
    let res2 = part2(&data);
    check_answer(&res2.to_string(), ans2, solved);
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
