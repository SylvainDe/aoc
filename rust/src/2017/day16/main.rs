use common::input::get_first_line_from_file;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2017_day16_input.txt";

type Int = u32;
type InputContent = String;

fn get_input_from_str(string: &str) -> InputContent {
    string.to_string()
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&get_first_line_from_file(filepath))
}

#[allow(clippy::missing_const_for_fn)]
fn part1(_arg: &InputContent) -> Int {
    0
}

#[allow(clippy::missing_const_for_fn)]
fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
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

    const EXAMPLE: &str = "";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 0);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
