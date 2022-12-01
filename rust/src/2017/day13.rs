use common::input::collect_from_lines;
use common::input::get_file_content;
use core::str::FromStr;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2017_day13_input.txt";

type Int = u32;

struct Layer {
    depth: Int,
    range: Int,
}

impl FromStr for Layer {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (depth, range) = s.split_once(": ").ok_or(())?;
        Ok(Self {
            depth: depth.parse().map_err(|_| {})?,
            range: range.parse().map_err(|_| {})?,
        })
    }
}

type InputContent = Vec<Layer>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

const fn is_caught(delay: Int, layer: &Layer) -> bool {
    // The period for a scanner is 2*(range-1)
    (layer.depth + delay) % (2 * (layer.range - 1)) == 0
}

const fn get_caught_score(layer: &Layer) -> Int {
    if is_caught(0, layer) {
        layer.depth * layer.range
    } else {
        0
    }
}

fn part1(layers: &InputContent) -> Int {
    layers.iter().map(get_caught_score).sum()
}

fn part2(layers: &InputContent) -> Int {
    // There may be a more mathematical approach to this
    for delay in 0.. {
        if layers.iter().all(|l| !is_caught(delay, l)) {
            return delay;
        }
    }
    0
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 1900);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 3_966_414);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "0: 3
1: 2
4: 4
6: 4";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 24);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 10);
    }
}
