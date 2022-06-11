use common::collect_from_lines;
use common::get_file_content;
use core::str::FromStr;
use std::collections::HashMap;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2021_day5_input.txt";

mod point_module {
    use core::str::FromStr;
    #[derive(Debug, PartialEq, Eq, Hash)]
    pub struct Point<T> {
        pub x: T,
        pub y: T,
    }

    impl<T: std::str::FromStr> FromStr for Point<T> {
        type Err = ();
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            let (x, y) = s.split_once(',').ok_or(())?;
            Ok(Self {
                x: x.parse().map_err(|_| {})?,
                y: y.parse().map_err(|_| {})?,
            })
        }
    }
}

type Int = i32;
type Point = point_module::Point<Int>;

#[derive(Debug, PartialEq)]
struct Vent {
    p1: Point,
    p2: Point,
}

impl FromStr for Vent {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (p1, p2) = s.split_once(" -> ").ok_or(())?;
        Ok(Self {
            p1: Point::from_str(p1)?,
            p2: Point::from_str(p2)?,
        })
    }
}

type InputContent = Vec<Vent>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string, Vent::from_str)
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&get_file_content(filepath))
}

#[allow(clippy::similar_names)]
fn count_intersection(vents: &Vec<Vent>, diagonal: bool) -> usize {
    let mut point_counter = HashMap::<Point, usize>::new();
    for Vent {
        p1: Point { x: x1, y: y1 },
        p2: Point { x: x2, y: y2 },
    } in vents
    {
        let dx = x2 - x1;
        let dy = y2 - y1;
        let absdx = dx.abs();
        let absdy = dy.abs();
        let mut step: Option<Int> = None;
        if dx == 0 {
            step = Some(absdy);
        } else if dy == 0 || (diagonal && absdx == absdy) {
            step = Some(absdx);
        }
        if let Some(step) = step {
            for s in 0..=step {
                let count = point_counter
                    .entry(Point {
                        x: x1 + s * dx / step,
                        y: y1 + s * dy / step,
                    })
                    .or_insert(0);
                *count += 1;
            }
        }
    }
    point_counter.iter().filter(|(_, &v)| v > 1).count()
}

fn part1(vents: &InputContent) -> usize {
    count_intersection(vents, false)
}

fn part2(vents: &InputContent) -> usize {
    count_intersection(vents, true)
}

fn main() {
    let before = Instant::now();
    let vents = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&vents);
    println!("{:?}", res);
    assert_eq!(res, 6225);
    let res2 = part2(&vents);
    println!("{:?}", res2);
    assert_eq!(res2, 22116);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2";

    #[test]
    fn test_point_from_str() {
        assert_eq!(Point::from_str("9,4"), Ok(Point { x: 9, y: 4 }));
    }

    #[test]
    fn point_from_str_invalid_values() {
        assert!(Point::from_str("9 4").is_err());
        assert!(Point::from_str("9, 4").is_err());
        assert!(Point::from_str("9,four").is_err());
    }

    #[test]
    fn test_vent_from_str() {
        assert_eq!(
            Vent::from_str("0,9 -> 5,9"),
            Ok(Vent {
                p1: Point { x: 0, y: 9 },
                p2: Point { x: 5, y: 9 }
            })
        );
    }

    #[test]
    fn test_vent_from_str_invalid_value() {
        assert!(Vent::from_str("0,9 ->5,9").is_err());
        assert!(Vent::from_str("0,9 -> 5 9").is_err());
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 5);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 12);
    }
}
