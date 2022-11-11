use common::get_first_line_from_file;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day19_input.txt";

type Int = u32;

fn get_input_from_str(string: &str) -> Int {
    string.parse().unwrap()
}

fn get_input_from_file(filepath: &str) -> Int {
    get_input_from_str(&get_first_line_from_file(filepath))
}

fn part1(size: Int) -> Int {
    // Naive implementation - "slow" but useful to check assumptions
    // Could be optimised with https://en.wikipedia.org/wiki/Josephus_problem
    let mut v = (1..=size).collect::<Vec<Int>>();
    let mut start = 0;
    while v.len() > 1 {
        let l = v.len();
        v = v.iter().skip(start).step_by(2).copied().collect();
        start = (start + l) % 2;
    }
    *v.first().unwrap()
}

#[allow(clippy::missing_const_for_fn)]
fn part2(_arg: Int) -> Int {
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(data);
    println!("{:?}", res);
    assert_eq!(res, 1_834_471);
    let res2 = part2(data);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "5";

    #[test]
    fn test_part1() {
        assert_eq!(part1(get_input_from_str(EXAMPLE)), 3);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(get_input_from_str(EXAMPLE)), 0);
    }
}
