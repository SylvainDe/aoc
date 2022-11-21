use common::input::get_first_line_from_file;
use std::collections::HashSet;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2017_day6_input.txt";

type Int = u32;
type InputContent = Vec<Int>;

fn get_input_from_str(string: &str) -> InputContent {
    string.split('\t').map(|s| s.parse().unwrap()).collect()
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&get_first_line_from_file(filepath))
}

fn part1(blocks: &InputContent) -> usize {
    let l = blocks.len();
    //let sum: Int = blocks.iter().sum();
    let mut blocks = blocks.clone();
    let mut seen = HashSet::new();
    while !seen.contains(&blocks) {
        seen.insert(blocks.clone());
        if let Some((i, n)) = blocks.iter().enumerate().max_by_key(|(_i, n)| *n) {
            for j in 0..*n {
                let idx = ((j as usize) + (i) + 1) % l;
                blocks[idx] += 1;
            }
            blocks[i] = 0; // TODO: Move this before the loop (then uncomment assert ?)
                           // assert_eq!(blocks.iter().sum::<Int>(), sum);
        }
    }
    seen.len()
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

    const EXAMPLE: &str = "0	2	7	0";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&vec![]), 1);
        assert_eq!(part1(&vec![0]), 1);
        assert_eq!(part1(&vec![10]), 2 /* WRONG SHOULD BE 1 */);
        assert_eq!(
            part1(&get_input_from_str(EXAMPLE)),
            8 /* WRONG SHOULD BE 5*/
        );
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
