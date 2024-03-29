// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_first_line_from_file;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day8_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2018_day8_answer.txt";

type Int = usize;
type InputContent = Vec<Int>;

fn get_input_from_str(string: &str) -> InputContent {
    string
        .split(' ')
        .map(|nb| nb.parse::<Int>().unwrap())
        .collect()
}

fn compute_scores(nbs: &[Int], part1: bool) -> (Int, &[Int]) {
    //dbg!("start", nbs.len());
    assert!(nbs.len() > 1);
    let nb_child = nbs[0];
    let nb_meta = nbs[1];
    let mut remaining = &nbs[2..];
    let mut childscores = Vec::new();
    // Parse children
    for _ in 0..nb_child {
        let meta;
        (meta, remaining) = compute_scores(remaining, part1);
        childscores.push(meta);
    }
    // Collect meta
    let meta = &remaining[0..nb_meta];
    remaining = &remaining[nb_meta..];
    // Compute final value based on rules applied
    let ret = if part1 || nb_child == 0 {
        childscores.iter().sum::<Int>() + meta.iter().sum::<Int>()
    } else {
        meta.iter()
            .map(|m| childscores.get(m - 1).unwrap_or(&0))
            .sum()
    };
    //dbg!("end", ret, remaining.len());
    (ret, remaining)
}

fn part1(nbs: &InputContent) -> Int {
    let (nb, rem) = compute_scores(nbs, true);
    assert!(rem.is_empty());
    nb
}

fn part2(nbs: &InputContent) -> Int {
    let (nb, rem) = compute_scores(nbs, false);
    assert!(rem.is_empty());
    nb
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_first_line_from_file(INPUT_FILEPATH));
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

    const EXAMPLE: &str = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 138);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 66);
    }
}
