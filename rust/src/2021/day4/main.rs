use std::collections::HashSet;
use std::fs;
use std::iter::zip;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2021_day4_input.txt";

type Int = u32;
type Grid = Vec<Vec<Int>>;

#[derive(Debug, PartialEq)]
struct BingoGame {
    numbers: Vec<Int>,
    grids: Vec<Grid>,
}

type InputContent = BingoGame;

fn get_input_from_str(string: &str) -> InputContent {
    let mut line_it = string.lines();
    let first_line = line_it.next().unwrap();
    let numbers: Vec<Int> = first_line
        .split(',')
        .map(|nb| nb.parse::<Int>().unwrap())
        .collect();
    line_it.next();
    let mut grids = Vec::<Grid>::new();
    let mut grid = Grid::new();
    for line in line_it {
        let l = line;
        if l.is_empty() {
            grids.push(grid);
            grid = Grid::new();
        } else {
            let nbs: Vec<Int> = l
                .split(' ')
                .filter(|s| !s.is_empty())
                .map(|s| s.parse::<Int>().unwrap())
                .collect();
            grid.push(nbs);
        }
    }
    grids.push(grid);
    BingoGame { numbers, grids }
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

#[derive(Debug, PartialEq, Clone)]
enum BingoState {
    InProgress,
    Finished(Int),
}

trait Scorable {
    fn compute_score(&self, numbers: &HashSet<Int>, last_number: Int) -> Int;
    fn score(&self, numbers: &HashSet<Int>, last_number: Int) -> BingoState;
}

impl Scorable for Grid {
    fn compute_score(&self, numbers: &HashSet<Int>, last_number: Int) -> Int {
        let mut s = 0;
        for line in self.iter() {
            for val in line.iter() {
                if !numbers.contains(val) {
                    s += val;
                }
            }
        }
        s * last_number
    }
    fn score(&self, numbers: &HashSet<Int>, last_number: Int) -> BingoState {
        // Look for horizontal lines
        for line in self.iter() {
            if !line.iter().any(|n| !numbers.contains(n)) {
                return BingoState::Finished(self.compute_score(numbers, last_number));
            }
        }
        // Look for vertical lines
        for i in 0..self[0].len() {
            if !self.iter().any(|l| !numbers.contains(&l[i])) {
                return BingoState::Finished(self.compute_score(numbers, last_number));
            }
        }
        BingoState::InProgress
    }
}

impl BingoGame {
    fn play(&self) -> Vec<Int> {
        // Store state (finished or not & score) for the different grids in a vector to
        // avoid rechecking already finished grids
        // A more efficient implementation could be to have a mapping from the numbers
        // to the places where they appear (grid number and position)
        let mut states = vec![BingoState::InProgress; self.grids.len()];
        let mut nbs = HashSet::<Int>::new();
        let mut scores = Vec::<Int>::new(); // I would have preferred a generator
        for n in &self.numbers {
            nbs.insert(*n);
            for (state, grid) in zip(states.iter_mut(), self.grids.iter()) {
                if *state == BingoState::InProgress {
                    let s = grid.score(&nbs, *n);
                    if let BingoState::Finished(score) = s {
                        *state = s;
                        scores.push(score);
                    }
                }
            }
        }
        scores
    }
}

fn part1(bingo: &InputContent) -> Int {
    bingo.play()[0]
}

fn part2(bingo: &InputContent) -> Int {
    *bingo.play().last().unwrap()
}

fn main() {
    let before = Instant::now();
    let bingo = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&bingo);
    println!("{:?}", res);
    assert_eq!(res, 50008);
    let res2 = part2(&bingo);
    println!("{:?}", res2);
    assert_eq!(res2, 17408);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7";

    #[test]
    fn test_play() {
        assert_eq!(get_input_from_str(EXAMPLE).play(), vec![4512, 2192, 1924]);
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 4512);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 1924);
    }
}
