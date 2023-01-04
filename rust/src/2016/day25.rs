// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::assembunny2016::get_input_from_str;
use common::assembunny2016::is_clock_signal;
use common::assembunny2016::Instructions;
use common::assembunny2016::Int;
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_file_content;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day25_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2016_day25_answer.txt";

fn part1(instructions: &Instructions) -> Int {
    for a in 1.. {
        if is_clock_signal(instructions, a) {
            return a;
        }
    }
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let (ans, _) = get_answers(ANSWERS_FILEPATH);
    let solved = false;
    let res = part1(&data);
    check_answer(&res.to_string(), ans, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}
