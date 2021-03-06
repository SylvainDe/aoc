use common::collect_from_lines;
use common::get_file_content;
use itertools::Itertools;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2021_day1_input.txt";

type Int = u32;
type InputContent = Vec<Int>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string, str::parse::<Int>)
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&get_file_content(filepath))
}

fn part1(depths: &InputContent) -> usize {
    depths.iter().tuple_windows().filter(|(a, b)| a < b).count()
}

fn part2(depths: &InputContent) -> usize {
    // Window(n + 1) > Window(n)
    // d(n+1) + d(n+2) + ... + d(n+1+windowsize) > d(n) + d(n+1) + ... + d(n+windowsize)
    // d(n+1+windowsize) > d(n)
    depths
        .iter()
        .tuple_windows()
        .filter(|(a, _, _, d)| a < d)
        .count()
}

fn main() {
    let before = Instant::now();
    let numbers = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&numbers);
    println!("{:?}", res);
    assert_eq!(res, 1832);
    let res2 = part2(&numbers);
    println!("{:?}", res2);
    assert_eq!(res2, 1858);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "199
200
208
210
200
207
240
269
260
263";

    #[test]
    fn input_from_str() {
        assert_eq!(
            get_input_from_str(EXAMPLE),
            vec![199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
        );
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 7);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 5);
    }
}
