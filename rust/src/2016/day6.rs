// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_file_content;
use std::collections::HashMap;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2016_day6_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2016_day6_answer.txt";

type Int = u32;
type InputContent = Vec<Vec<char>>;

fn get_input_from_str(string: &str) -> InputContent {
    string.lines().map(|l| l.chars().collect()).collect()
}

fn transpose(v: &InputContent) -> InputContent {
    assert!(!v.is_empty(), "Cannot transpose empty matrix");
    let len = v[0].len();
    (0..len)
        .map(|i| v.iter().map(|row| row[i]).collect())
        .collect()
}

// TODO: Make types more generic
fn count(v: &Vec<char>) -> HashMap<char, Int> {
    let mut counter = HashMap::new();
    for c in v {
        let count = counter.entry(*c).or_insert(0);
        *count += 1;
    }
    counter
}

fn part1(arg: &InputContent) -> String {
    transpose(arg)
        .iter()
        .map(|col| {
            count(col)
                .into_iter()
                .max_by_key(|&(_, count)| count)
                .unwrap()
                .0
        })
        .collect()
}

fn part2(arg: &InputContent) -> String {
    transpose(arg)
        .iter()
        .map(|col| {
            count(col)
                .into_iter()
                .min_by_key(|&(_, count)| count)
                .unwrap()
                .0
        })
        .collect()
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(&data);
    check_answer(&res, ans, solved);
    let res2 = part2(&data);
    check_answer(&res2, ans2, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), "easter");
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), "advent");
    }
}
