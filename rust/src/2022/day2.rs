// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::get_file_content;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2022_day2_input.txt";

type Int = u32;
type GameInput = (char, char);
type InputContent = Vec<GameInput>;

fn get_input_from_str(string: &str) -> InputContent {
    string
        .lines()
        .map(|l| {
            let s = l
                .split(' ')
                .map(|c| c.chars().next().unwrap())
                .collect::<Vec<char>>();
            (s[0], s[1])
        })
        .collect()
}

// This implementation relies heavily on enumeration and contains a lot
// of boilerplate code. Alternatives could be:
//  - rely on mapping (shape, shape) -> outcome and (shape, outcome) -> shape
enum Shape {
    Rock,
    Paper,
    Scissors,
}

enum Outcome {
    Lose,
    Draw,
    Win,
}

/* Rules */
const fn play_game(opponent: &Shape, me: &Shape) -> Outcome {
    match (opponent, me) {
        (Shape::Rock, Shape::Rock)
        | (Shape::Paper, Shape::Paper)
        | (Shape::Scissors, Shape::Scissors) => Outcome::Draw,
        (Shape::Rock, Shape::Paper)
        | (Shape::Paper, Shape::Scissors)
        | (Shape::Scissors, Shape::Rock) => Outcome::Win,
        (Shape::Rock, Shape::Scissors)
        | (Shape::Paper, Shape::Rock)
        | (Shape::Scissors, Shape::Paper) => Outcome::Lose,
    }
}

const fn get_shape_to_play(opponent: &Shape, outcome: &Outcome) -> Shape {
    match (opponent, outcome) {
        (Shape::Rock, Outcome::Lose)
        | (Shape::Scissors, Outcome::Draw)
        | (Shape::Paper, Outcome::Win) => Shape::Scissors,
        (Shape::Paper, Outcome::Lose)
        | (Shape::Rock, Outcome::Draw)
        | (Shape::Scissors, Outcome::Win) => Shape::Rock,
        (Shape::Scissors, Outcome::Lose)
        | (Shape::Paper, Outcome::Draw)
        | (Shape::Rock, Outcome::Win) => Shape::Paper,
    }
}

/* Input parsing */
fn get_shape(c: char) -> Shape {
    match c {
        'A' | 'X' => Shape::Rock,
        'B' | 'Y' => Shape::Paper,
        'C' | 'Z' => Shape::Scissors,
        _ => panic!("Unexpected char"),
    }
}

fn get_outcome(c: char) -> Outcome {
    match c {
        'X' => Outcome::Lose,
        'Y' => Outcome::Draw,
        'Z' => Outcome::Win,
        _ => panic!("Unexpected char"),
    }
}

/* Scores */
const fn shape_score(shape: &Shape) -> Int {
    match shape {
        Shape::Rock => 1,
        Shape::Paper => 2,
        Shape::Scissors => 3,
    }
}

const fn outcome_score(outcome: &Outcome) -> Int {
    match outcome {
        Outcome::Lose => 0,
        Outcome::Draw => 3,
        Outcome::Win => 6,
    }
}

const fn game_score(opponent: &Shape, me: &Shape) -> Int {
    shape_score(me) + outcome_score(&play_game(opponent, me))
}

const fn game_score2(opponent: &Shape, outcome: &Outcome) -> Int {
    let me = get_shape_to_play(opponent, outcome);
    shape_score(&me) + outcome_score(outcome)
}

fn part1(games: &InputContent) -> Int {
    games
        .iter()
        .map(|(a, b)| game_score(&get_shape(*a), &get_shape(*b)))
        .sum()
}

fn part2(games: &InputContent) -> Int {
    games
        .iter()
        .map(|(a, b)| game_score2(&get_shape(*a), &get_outcome(*b)))
        .sum()
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let res = part1(&data);
    println!("{:?}", res);
    assert_eq!(res, 14264);
    let res2 = part2(&data);
    println!("{:?}", res2);
    assert_eq!(res2, 12382);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "A Y
B X
C Z";

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 15);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 12);
    }
}
