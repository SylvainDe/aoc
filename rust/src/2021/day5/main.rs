use core::str::FromStr;
use std::collections::HashMap;
use std::fs;

const INPUT_FILEPATH: &str = "res/2021/day5/input.txt";

type Int = u32;

#[derive(Debug, PartialEq, Eq, Hash)]
struct Point {
    x: Int,
    y: Int,
}

impl FromStr for Point {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (x, y) = s.split_once(',').ok_or(())?;
        Ok(Point {
            x: x.parse().map_err(|_| {})?,
            y: y.parse().map_err(|_| {})?,
        })
    }
}

#[derive(Debug, PartialEq)]
struct Vent {
    p1: Point,
    p2: Point,
}

impl FromStr for Vent {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let (p1, p2) = s.split_once(" -> ").ok_or(())?;
        Ok(Vent {
            p1: Point::from_str(p1)?,
            p2: Point::from_str(p2)?,
        })
    }
}

fn get_input_from_str(s: &str) -> Vec<Vent> {
    s.lines()
        .map(|line| Vent::from_str(line).unwrap())
        .collect()
}

fn get_input_from_file(filepath: &str) -> Vec<Vent> {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

fn part1(vents: &Vec<Vent>) -> usize {
    let mut point_counter = HashMap::<Point, usize>::new();
    for Vent {
        p1: Point { x: x1, y: y1 },
        p2: Point { x: x2, y: y2 },
    } in vents
    {
        if x1 == x2 {
            let (min, max) = if y1 < y2 { (y1, y2) } else { (y2, y1) };
            for y in *min..=*max {
                let count = point_counter.entry(Point { x: *x1, y }).or_insert(0);
                *count += 1;
            }
        } else if y1 == y2 {
            let (min, max) = if x1 < x2 { (x1, x2) } else { (x2, x1) };
            for x in *min..=*max {
                let count = point_counter.entry(Point { x, y: *y1 }).or_insert(0);
                *count += 1;
            }
        }
    }
    point_counter.iter().filter(|(_, &v)| v > 1).count()
}

fn part2(_vents: &[Vent]) -> Int {
    0
}

fn main() {
    let vents = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&vents);
    println!("{:?}", res);
    assert_eq!(res, 6225);
    let res2 = part2(&vents);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
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
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
