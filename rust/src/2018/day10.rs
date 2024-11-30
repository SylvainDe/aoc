// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::collect_from_lines;
use common::input::get_answers;
use common::input::get_file_content;
use common::point_module;
use core::str::FromStr;
use itertools::Itertools as _;
use lazy_static::lazy_static;
use regex::Regex;
use std::collections::HashMap;
use std::collections::HashSet;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2018_day10_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2018_day10_answer.txt";

type Int = i32;
type Point = point_module::Point<Int>;

#[derive(Debug, PartialEq)]
struct Star {
    position: Point,
    velocity: Point,
}

impl FromStr for Star {
    type Err = ();
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        // "position=< 9,  1> velocity=< 0,  2>"
        lazy_static! {
            static ref RE: Regex =
                Regex::new(r"^position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>$")
                    .unwrap();
        }
        let c = RE.captures(s).ok_or(())?;
        let to_int = |i: usize| c.get(i).ok_or(())?.as_str().parse::<Int>().map_err(|_| {});
        Ok(Self {
            position: Point {
                x: to_int(1)?,
                y: to_int(2)?,
            },
            velocity: Point {
                x: to_int(3)?,
                y: to_int(4)?,
            },
        })
    }
}

type InputContent = Vec<Star>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_from_lines(string)
}

fn get_positions(stars: &InputContent, steps: Int) -> Vec<(Int, Int)> {
    stars
        .iter()
        .map(
            |Star {
                 position: Point { x: px, y: py },
                 velocity: Point { x: vx, y: vy },
             }| (px + vx * steps, py + vy * steps),
        )
        .collect()
}

fn show_stars(positions: &Vec<(Int, Int)>) -> Option<String> {
    if positions.is_empty() {
        return None;
    }
    let xs = positions.iter().map(|(x, _)| *x).collect::<Vec<Int>>();
    let ys = positions.iter().map(|(_, y)| *y).collect::<Vec<Int>>();
    let x_min = *xs.iter().min().unwrap();
    let x_max = *xs.iter().max().unwrap();
    let y_min = *ys.iter().min().unwrap();
    let y_max = *ys.iter().max().unwrap();
    let dx = x_max - x_min;
    let dy = y_max - y_min;
    if dx > 80 || dy > 15 {
        return None;
    }

    let mut points: HashMap<Int, HashSet<Int>> = HashMap::new();
    for (x, y) in positions {
        points.entry(*y).or_default().insert(*x);
    }
    Some(
        (y_min..=y_max)
            .map(|y| get_line(points.entry(y).or_default(), x_min, x_max))
            .join("\n"),
    )
}

fn get_line(set: &HashSet<Int>, val_min: Int, val_max: Int) -> String {
    (val_min..=val_max)
        .map(|v| if set.contains(&v) { '#' } else { '.' })
        .collect()
}

fn find_pattern(stars: &InputContent) -> (String, Int) {
    // This could be optimised with maths...
    for i in 0..=11000 {
        if let Some(s) = show_stars(&get_positions(stars, i)) {
            return (s, i);
        }
    }
    ("Not found".to_owned(), 0)
}

fn part1(stars: &InputContent) -> String {
    find_pattern(stars).0
}

fn part2(stars: &InputContent) -> Int {
    find_pattern(stars).1
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let (_, ans2) = get_answers(ANSWERS_FILEPATH);
    let ans = Some(
        "#####...#.......######..######..#....#..#####.....##....#....#
#....#..#.......#............#..##...#..#....#...#..#...##...#
#....#..#.......#............#..##...#..#....#..#....#..##...#
#....#..#.......#...........#...#.#..#..#....#..#....#..#.#..#
#####...#.......#####......#....#.#..#..#####...#....#..#.#..#
#..#....#.......#.........#.....#..#.#..#..#....######..#..#.#
#...#...#.......#........#......#..#.#..#...#...#....#..#..#.#
#...#...#.......#.......#.......#...##..#...#...#....#..#...##
#....#..#.......#.......#.......#...##..#....#..#....#..#...##
#....#..######..######..######..#....#..#....#..#....#..#....#"
            .to_owned(),
    );
    let solved = true;
    let res = part1(&data);
    check_answer(&res, ans, solved);
    let res2 = part2(&data);
    check_answer(&res2.to_string(), ans2, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>";

    #[test]
    fn test_star_from_star() {
        assert_eq!(
            Star::from_str("position=< 3, -2> velocity=<-1,  1>"),
            Ok(Star {
                position: Point { x: 3, y: -2 },
                velocity: Point { x: -1, y: 1 },
            },)
        );
    }

    #[test]
    fn test_show_hi() {
        assert_eq!(
            show_stars(&get_positions(&get_input_from_str(EXAMPLE), 3)),
            Some(
                "#...#..###
#...#...#.
#...#...#.
#####...#.
#...#...#.
#...#...#.
#...#...#.
#...#..###"
                    .to_owned()
            )
        );
    }
}
