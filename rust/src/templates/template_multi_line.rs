// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::collect_lines;
use common::input::get_file_content;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/yearYYYY_dayDD_input.txt";

type Int = u32;
type InputContent = Vec<String>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_lines(string)
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
