// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_from_lines;
use common::input::get_answers;
use common::input::get_file_content;
use common::point_module;
use core::str::FromStr;
use std::collections::HashMap;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2021_day5_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2021_day5_answer.txt";

type Int = i32;
type Point = point_module::Point<Int>;

#[derive(Debug, PartialEq)]
struct Vent {
    p1: Point,
    p2: Point,
}

impl FromStr for Vent {
    type Err = point_module::FromStrError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (p1, p2) = s.split_once(" -> ").ok_or(point_module::FromStrError)?;
        Ok(Self {
            p1: Point::from_str_with_param(p1, ",")?,
            p2: Point::from_str_with_param(p2, ",")?,
        })
    }
}

type InputContent = Vec<Vent>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

#[expect(clippy::similar_names, reason = "Mathematical computations")]
fn count_intersection(vents: &Vec<Vent>, diagonal: bool) -> usize {
    let mut point_counter = HashMap::new();
    for Vent {
        p1: Point { x: x1, y: y1 },
        p2: Point { x: x2, y: y2 },
    } in vents
    {
        let dx = x2 - x1;
        let dy = y2 - y1;
        let absdx = dx.abs();
        let absdy = dy.abs();
        let mut step = None;
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
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
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
