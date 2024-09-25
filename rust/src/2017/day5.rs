// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_from_lines;
use common::input::get_answers;
use common::input::get_file_content;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2017_day5_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2017_day5_answer.txt";

type Int = i32;
type InputContent = Vec<Int>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

#[expect(clippy::cast_sign_loss, reason = "cast between Int (i32) and usize")]
fn count_steps(instructions: &InputContent, new_rule: bool) -> Int {
    let mut instructions = instructions.clone();
    let mut pos = 0;
    let mut steps = 0;
    while let Some(&n) = &instructions.get(pos as usize) {
        instructions[pos as usize] = if new_rule && n >= 3 { n - 1 } else { n + 1 };
        pos += n;
        steps += 1;
    }
    steps
}

fn part1(instructions: &InputContent) -> Int {
    count_steps(instructions, false)
}

fn part2(instructions: &InputContent) -> Int {
    count_steps(instructions, true)
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

    const EXAMPLE: &str = "0
3
0
1
-3";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 5);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 10);
    }
}
