// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::get_first_line_from_file;
use std::collections::HashMap;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2017_day6_input.txt";

type Int = u32;
type InputContent = Vec<Int>;

fn get_input_from_str(string: &str) -> InputContent {
    string.split('\t').map(|s| s.parse().unwrap()).collect()
}

#[allow(clippy::cast_sign_loss)]
fn get_cycle_information(blocks: &InputContent) -> (usize, usize) {
    let l = blocks.len();
    let sum: Int = blocks.iter().sum();
    let mut blocks = blocks.clone();
    let mut seen = HashMap::<InputContent, usize>::new();
    let mut i = 0;
    loop {
        if let Some(index) = seen.get(&blocks) {
            return (i, i - index);
        }
        seen.insert(blocks.clone(), i);
        if let Some((i, &n)) = blocks
            .iter()
            .enumerate()
            .min_by_key(|(_i, &n)| -(i64::from(n)))
        {
            blocks[i] = 0;
            for j in 0..n {
                let idx = ((j as usize) + (i) + 1) % l;
                blocks[idx] += 1;
            }
            assert_eq!(blocks.iter().sum::<Int>(), sum);
        }
        i += 1;
    }
}

fn part1(blocks: &InputContent) -> usize {
    get_cycle_information(blocks).0
}

fn part2(blocks: &InputContent) -> usize {
    get_cycle_information(blocks).1
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_first_line_from_file(INPUT_FILEPATH));
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 6681);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 2392);
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
        assert_eq!(part1(&vec![10]), 1);
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 5);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 4);
    }
}
