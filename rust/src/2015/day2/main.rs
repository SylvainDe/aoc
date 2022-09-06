use common::collect_from_lines;
use common::get_file_content;
use core::str::FromStr;
use itertools::min;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2015_day2_input.txt";

type Int = u32;
#[derive(Debug, PartialEq)]
struct BoxDimensions {
    l: Int,
    w: Int,
    h: Int,
}
type InputContent = Vec<BoxDimensions>;

impl FromStr for BoxDimensions {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (l, s) = s.split_once('x').ok_or(())?;
        let (w, h) = s.split_once('x').ok_or(())?;
        Ok(Self {
            l: l.parse().map_err(|_| {})?,
            w: w.parse().map_err(|_| {})?,
            h: h.parse().map_err(|_| {})?,
        })
    }
}

impl BoxDimensions {
    fn paper(&self) -> Int {
        let Self { l, w, h } = self;
        let sides = [l * w, l * h, w * h];
        2 * (sides.iter().sum::<Int>()) + min(sides).unwrap()
    }
    fn ribbon(&self) -> Int {
        let Self { l, w, h } = self;
        let peri = [l + w, l + h, w + h];
        2 * min(peri).unwrap() + l * w * h
    }
}

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string, BoxDimensions::from_str)
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&get_file_content(filepath))
}

fn part1(input: &InputContent) -> Int {
    input.iter().map(BoxDimensions::paper).sum()
}

fn part2(input: &InputContent) -> Int {
    input.iter().map(BoxDimensions::ribbon).sum()
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 1_586_300);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 3_737_498);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dimensions_from_str() {
        assert!(BoxDimensions::from_str("").is_err());
        assert_eq!(
            BoxDimensions::from_str("1x2x3"),
            Ok(BoxDimensions { l: 1, w: 2, h: 3 })
        );
    }
    #[test]
    fn test_paper() {
        assert_eq!(BoxDimensions { l: 2, w: 3, h: 4 }.paper(), 58);
        assert_eq!(BoxDimensions { l: 1, w: 1, h: 10 }.paper(), 43);
    }

    #[test]
    fn test_ribbon() {
        assert_eq!(BoxDimensions { l: 2, w: 3, h: 4 }.ribbon(), 34);
        assert_eq!(BoxDimensions { l: 1, w: 1, h: 10 }.ribbon(), 14);
    }
}
