// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_first_line_from_file;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day14_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2018_day14_answer.txt";

type Int = usize;

fn slice_to_int(vec: &[Int]) -> Int {
    let mut res = 0;
    for n in vec {
        res = 10 * res + n;
    }
    res
}

fn part1(nb_recipe: &str) -> Int {
    let nb_recipe = nb_recipe.parse().unwrap();
    let mut scores = Vec::from([3, 7]);
    let mut e1 = 0;
    let mut e2 = 1;
    let nb_recipe_required = nb_recipe + 10;
    while scores.len() < nb_recipe_required {
        let old_s1 = scores[e1];
        let old_s2 = scores[e2];
        let s = old_s1 + old_s2;
        let s1 = s / 10;
        let s2 = s % 10;
        if s1 > 0 {
            scores.push(s1);
        }
        scores.push(s2);
        let l = scores.len();
        e1 = (e1 + old_s1 + 1) % l;
        e2 = (e2 + old_s2 + 1) % l;
    }
    slice_to_int(&scores[nb_recipe..nb_recipe + 10])
}

fn part2(expected_score: &str) -> Int {
    let mut scores = Vec::from([3, 7]);
    let mut e1 = 0;
    let mut e2 = 1;
    let expected_vec: Vec<Int> = expected_score
        .chars()
        .map(|c| c.to_digit(10).unwrap() as usize)
        .collect();
    let expected_len = expected_vec.len();
    loop {
        let old_s1 = scores[e1];
        let old_s2 = scores[e2];
        let s = old_s1 + old_s2;
        let s1 = s / 10;
        let s2 = s % 10;
        if s1 > 0 {
            scores.push(s1);
            if scores.len() >= expected_len && scores[scores.len() - expected_len..] == expected_vec
            {
                return scores.len() - expected_len;
            }
        }
        scores.push(s2);
        if scores.len() >= expected_len && scores[scores.len() - expected_len..] == expected_vec {
            return scores.len() - expected_len;
        }
        let l = scores.len();
        e1 = (e1 + old_s1 + 1) % l;
        e2 = (e2 + old_s2 + 1) % l;
    }
}

fn main() {
    let before = Instant::now();
    let data = &get_first_line_from_file(INPUT_FILEPATH);
    let (ans, ans2) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(data);
    check_answer(&res.to_string(), ans, solved);
    let res2 = part2(data);
    check_answer(&res2.to_string(), ans2, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        assert_eq!(part1("5"), 124515891);
        assert_eq!(part1("18"), 9251071085);
        assert_eq!(part1("2018"), 5941429882);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2("51589"), 9);
        assert_eq!(part2("01245"), 5);
        assert_eq!(part2("92510"), 18);
        assert_eq!(part2("59414"), 2018);
    }
}
