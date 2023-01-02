// vi: set shiftwidth=4 tabstop=4 expandtab:
use common::input::check_answer;
use common::input::get_answers;
use common::input::get_first_line_from_file;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2015_day25_input.txt";
const ANSWERS_FILEPATH: &str = "../resources/year2015_day25_answer.txt";

type Int = u64;
type InputContent = (Int, Int);

const fn get_input_from_str(_string: &str) -> InputContent {
    // TODO: Parse string
    (2978, 3083)
}

const fn get_index(pos: (Int, Int)) -> Int {
    let (row, col) = pos;
    let n = row + col - 2;
    col + n * (n + 1) / 2
}

// From https://rob.co.bb/posts/2019-02-10-modular-exponentiation-in-rust/
const fn mod_pow(mut base: Int, mut exp: Int, modulus: Int) -> Int {
    if modulus == 1 {
        return 0;
    }
    let mut result = 1;
    base %= modulus;
    while exp > 0 {
        if exp % 2 == 1 {
            result = result * base % modulus;
        }
        exp >>= 1;
        base = base * base % modulus;
    }
    result
}

const fn get_code_at_index(n: Int, start: Int, mult: Int, modulus: Int) -> Int {
    (start * mod_pow(mult, n - 1, modulus)) % modulus
}

const fn part1(pos: InputContent) -> Int {
    get_code_at_index(get_index(pos), 20_151_125, 252_533, 33_554_393)
}

fn main() {
    let before = Instant::now();
    let data = get_input_from_str(&get_first_line_from_file(INPUT_FILEPATH));
    let (ans, _) = get_answers(ANSWERS_FILEPATH);
    let solved = true;
    let res = part1(data);
    check_answer(&res.to_string(), ans, solved);
    println!("Elapsed time: {:.2?}", before.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_functions() {
        assert_eq!(get_index((4, 2)), 12);
        assert_eq!(get_index((1, 5)), 15);
        // TODO: Add more
    }
}
