// First line
// vi: set shiftwidth=4 tabstop=4 expandtab:

pub mod input {
    use std::borrow::ToOwned;
    use std::fmt::Debug;
    use std::fs;
    use std::str::FromStr;

    #[must_use]
    pub fn get_first_line(string: &str) -> String {
        string.lines().next().map_or("", |l| l).to_owned()
    }

    /// # Panics
    ///
    /// Will panic if file can't be read
    #[must_use]
    pub fn get_file_content(filepath: &str) -> String {
        fs::read_to_string(filepath).expect("Could not open file")
    }

    #[must_use]
    pub fn get_first_line_from_file(filepath: &str) -> String {
        get_first_line(&get_file_content(filepath))
    }

    #[must_use]
    pub fn collect_lines(string: &str) -> Vec<String> {
        string.lines().map(ToOwned::to_owned).collect()
    }

    /// # Panics
    ///
    /// Will panic if call to F fails on a element
    #[must_use]
    pub fn collect_from_lines_with_func<Item, F, E>(string: &str, f: F) -> Vec<Item>
    where
        F: Fn(&str) -> Result<Item, E>,
        E: Debug,
    {
        string.lines().map(|l| f(l).unwrap()).collect()
    }

    /// # Panics
    ///
    /// Will panic if call to F fails on a element
    #[must_use]
    pub fn collect_from_lines<A: FromStr>(string: &str) -> Vec<A>
    where
        <A as FromStr>::Err: Debug,
    {
        string.lines().map(|l| A::from_str(l).unwrap()).collect()
    }

    #[must_use]
    pub fn get_answers(filepath: &str) -> (Option<String>, Option<String>) {
        fs::read_to_string(filepath).map_or((None, None), |s| {
            let v: Vec<String> = s.lines().map(ToOwned::to_owned).collect();
            (v.first().cloned(), v.get(1).cloned())
        })
    }

    /// # Panics
    ///
    /// Will panic if answers do not match in strict mode
    pub fn check_answer(result: &str, expected: Option<String>, is_strict: bool) {
        expected.map_or_else(
            || println!("Result: {result}"),
            |expected_res| {
                if is_strict {
                    // println!("Answer: {} (expected: {})", result, expected_res);
                    assert_eq!(result, expected_res, "Invalid answer computed");
                } else if result == expected_res {
                    println!("Correct answer: {result}");
                } else {
                    println!("Incorrect answer: {result} (expected {expected_res})");
                }
            },
        );
    }
}

pub mod point_module {
    use std::ops::{Add, Sub};
    use std::str::FromStr;

    #[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
    pub struct Point<T> {
        pub x: T,
        pub y: T,
    }

    #[derive(Debug, PartialEq, Eq, Hash)]
    pub struct FromStrError;

    impl<T: FromStr> Point<T> {
        #[allow(clippy::result_unit_err, clippy::missing_errors_doc)]
        pub fn from_str_with_param(s: &str, separator: &str) -> Result<Self, FromStrError> {
            let (x, y) = s.split_once(separator).ok_or(FromStrError)?;
            Ok(Self {
                x: x.parse().map_err(|_| FromStrError)?,
                y: y.parse().map_err(|_| FromStrError)?,
            })
        }
    }

    impl<T: FromStr> FromStr for Point<T> {
        type Err = ();
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            let (x, y) = s.split_once(", ").ok_or(())?;
            Ok(Self {
                x: x.parse().map_err(|_| {})?,
                y: y.parse().map_err(|_| {})?,
            })
        }
    }

    // Directly copied from https://doc.rust-lang.org/std/ops/index.html
    impl<T: Add<Output = T>> Add for Point<T> {
        type Output = Self;

        fn add(self, other: Self) -> Self {
            Self {
                x: self.x + other.x,
                y: self.y + other.y,
            }
        }
    }

    impl<T: Sub<Output = T>> Sub for Point<T> {
        type Output = Self;

        fn sub(self, other: Self) -> Self {
            Self {
                x: self.x - other.x,
                y: self.y - other.y,
            }
        }
    }
}

#[cfg(test)]
mod tests_input {
    use crate::input::{get_first_line, get_first_line_from_file};

    #[test]
    fn test_get_first_line() {
        assert_eq!(get_first_line(""), "");
        assert_eq!(get_first_line("abc\n"), "abc");
        assert_eq!(get_first_line("abc\ndef"), "abc");
        assert_eq!(get_first_line("abc\ndef\n"), "abc");
    }

    #[test]
    fn test_get_first_line_from_file() {
        assert_eq!(
            get_first_line_from_file("src/lib/common.rs"),
            "// First line"
        );
    }
}

#[cfg(test)]
mod tests_point {
    use crate::point_module::Point;
    use std::str::FromStr;

    #[test]
    fn test_point_from_str() {
        assert_eq!(
            Point::from_str_with_param("9, 4", ", "),
            Ok(Point { x: 9, y: 4 })
        );
        assert_eq!(
            Point::from_str_with_param("9,4", ","),
            Ok(Point { x: 9, y: 4 })
        );
        assert_eq!(Point::from_str("9, 4"), Ok(Point { x: 9, y: 4 }));
    }

    #[test]
    fn point_from_str_invalid_values() {
        assert!(Point::<i32>::from_str_with_param("9 4", ", ").is_err());
        assert!(Point::<i32>::from_str_with_param("9,4", ", ").is_err());
        assert!(Point::<i32>::from_str_with_param("9, 4", ",").is_err());
        assert!(Point::<i32>::from_str_with_param("9,four", ", ").is_err());
        assert!(Point::<i32>::from_str_with_param("9 4", ",").is_err());
        assert!(Point::<i32>::from_str_with_param("9, 4", ",").is_err());
        assert!(Point::<i32>::from_str_with_param("9,four", ",").is_err());

        assert!(Point::<i32>::from_str("9 4").is_err());
        assert!(Point::<i32>::from_str("9,4").is_err());
        assert!(Point::<i32>::from_str("9,four").is_err());
    }

    #[test]
    fn point_operations() {
        assert_eq!(
            Point { x: 3, y: 3 },
            Point { x: 1, y: 0 } + Point { x: 2, y: 3 }
        );
        assert_eq!(
            Point { x: -1, y: -3 },
            Point { x: 1, y: 0 } - Point { x: 2, y: 3 }
        );
    }
}

pub mod assembunny2016 {
    use crate::input::collect_from_lines;
    use std::collections::HashMap;
    use std::collections::HashSet;
    use std::str::FromStr;
    pub type Int = i32;
    pub type Instructions = Vec<Instruction>;

    #[derive(Debug, Eq, Ord, PartialEq, PartialOrd, Hash, Clone)]
    pub enum Instruction {
        Copy(String, String),
        Increase(String),
        Decrease(String),
        Jump(String, String),
        Toggle(String),
        Transmit(String),
    }

    impl FromStr for Instruction {
        type Err = ();
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            let chunks: Vec<&str> = s.split(' ').collect();
            match chunks.first() {
                None => (),
                Some(&cmd) => match cmd {
                    "inc" => {
                        if chunks.len() == 2 {
                            return Ok(Self::Increase(chunks[1].to_owned()));
                        }
                    }
                    "dec" => {
                        if chunks.len() == 2 {
                            return Ok(Self::Decrease(chunks[1].to_owned()));
                        }
                    }
                    "tgl" => {
                        if chunks.len() == 2 {
                            return Ok(Self::Toggle(chunks[1].to_owned()));
                        }
                    }
                    "out" => {
                        if chunks.len() == 2 {
                            return Ok(Self::Transmit(chunks[1].to_owned()));
                        }
                    }
                    "cpy" => {
                        if chunks.len() == 3 {
                            return Ok(Self::Copy(chunks[1].to_owned(), chunks[2].to_owned()));
                        }
                    }
                    "jnz" => {
                        if chunks.len() == 3 {
                            return Ok(Self::Jump(chunks[1].to_owned(), chunks[2].to_owned()));
                        }
                    }
                    _ => (),
                },
            }
            Err(())
        }
    }

    #[must_use]
    pub fn get_input_from_str(string: &str) -> Instructions {
        collect_from_lines(string)
    }

    #[allow(clippy::missing_const_for_fn)]
    fn toggle_ins(ins: Instruction) -> Instruction {
        match ins {
            // For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc
            Instruction::Increase(x) => Instruction::Decrease(x),
            Instruction::Decrease(x) | Instruction::Toggle(x) | Instruction::Transmit(x) => {
                Instruction::Increase(x)
            }
            // For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz
            Instruction::Jump(x, y) => Instruction::Copy(x, y),
            Instruction::Copy(x, y) => Instruction::Jump(x, y),
        }
    }

    fn eval_string(s: &str, env: &HashMap<String, Int>) -> Int {
        s.parse::<Int>().unwrap_or_else(|_| *env.get(s).unwrap())
    }

    /// # Panics
    ///
    /// Will panic if something goes wrong
    #[must_use]
    #[allow(clippy::cast_sign_loss)]
    pub fn run_instructions(instructions: &Instructions, a_value: Int, c_value: Int) -> Int {
        let mut instructions = instructions.clone();
        let mut env = HashMap::from([
            ("a".to_owned(), a_value),
            ("b".to_owned(), 0),
            ("c".to_owned(), c_value),
            ("d".to_owned(), 0),
        ]);
        let mut cnt = 0;
        while let Some(ins) = instructions.get(cnt as usize) {
            match ins {
                Instruction::Copy(x, y) => {
                    let x = eval_string(x, &env);
                    env.insert(y.clone(), x);
                }
                Instruction::Increase(x) => {
                    env.entry(x.clone()).and_modify(|e| *e += 1);
                }
                Instruction::Decrease(x) => {
                    env.entry(x.clone()).and_modify(|e| *e -= 1);
                }
                Instruction::Toggle(x) => {
                    let x = eval_string(x, &env);
                    let pos = (cnt + x) as usize;
                    if let Some(ins2) = instructions.get(pos) {
                        instructions[pos] = toggle_ins(ins2.clone());
                    }
                }
                Instruction::Jump(x, y) => {
                    let x = eval_string(x, &env);
                    if x != 0 {
                        let y = eval_string(y, &env);
                        cnt += y;
                        continue;
                    }
                }
                Instruction::Transmit(_) => (),
            }
            cnt += 1;
        }
        env["a"]
    }

    /// # Panics
    ///
    /// Will panic if something goes wrong
    #[must_use]
    #[allow(clippy::cast_sign_loss)]
    pub fn is_clock_signal(instructions: &Instructions, a_value: Int) -> bool {
        let mut instructions = instructions.clone();
        let mut env = HashMap::from([
            ("a".to_owned(), a_value),
            ("b".to_owned(), 0),
            ("c".to_owned(), 0),
            ("d".to_owned(), 0),
        ]);
        let mut expected = 0;
        let mut seen = HashSet::new();
        let mut cnt = 0;
        while let Some(ins) = instructions.get(cnt as usize) {
            match ins {
                Instruction::Copy(x, y) => {
                    let x = eval_string(x, &env);
                    env.insert(y.clone(), x);
                }
                Instruction::Increase(x) => {
                    env.entry(x.clone()).and_modify(|e| *e += 1);
                }
                Instruction::Decrease(x) => {
                    env.entry(x.clone()).and_modify(|e| *e -= 1);
                }
                Instruction::Toggle(x) => {
                    let x = eval_string(x, &env);
                    let pos = (cnt + x) as usize;
                    if let Some(ins2) = instructions.get(pos) {
                        instructions[pos] = toggle_ins(ins2.clone());
                    }
                }
                Instruction::Jump(x, y) => {
                    let x = eval_string(x, &env);
                    if x != 0 {
                        let y = eval_string(y, &env);
                        cnt += y;
                        continue;
                    }
                }
                Instruction::Transmit(x) => {
                    let x = eval_string(x, &env);
                    if x != expected {
                        return false;
                    }
                    if expected == 0 {
                        let state = (
                            env["a"],
                            env["b"],
                            env["c"],
                            env["d"],
                            cnt,
                            instructions.clone(),
                        );
                        if seen.contains(&state) {
                            return true;
                        }
                        seen.insert(state);
                    }
                    expected = Int::from(expected == 0);
                }
            }
            cnt += 1;
        }
        false
    }
}

#[cfg(test)]
mod tests_assembunny2016 {
    use crate::assembunny2016::{run_instructions, Instruction};
    use crate::input::collect_from_lines;
    use core::str::FromStr;

    const EXAMPLE_DAY_12: &str = "cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a";

    const EXAMPLE_DAY_23: &str = "cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a";

    #[test]
    fn test_instruction_from_str() {
        assert_eq!(
            Instruction::from_str("cpy 41 a"),
            Ok(Instruction::Copy("41".to_owned(), "a".to_owned()))
        );
        assert_eq!(
            Instruction::from_str("jnz a 2"),
            Ok(Instruction::Jump("a".to_owned(), "2".to_owned()))
        );
        assert_eq!(
            Instruction::from_str("inc a"),
            Ok(Instruction::Increase("a".to_owned()))
        );
        assert_eq!(
            Instruction::from_str("dec a"),
            Ok(Instruction::Decrease("a".to_owned()))
        );
        assert_eq!(
            Instruction::from_str("tgl a"),
            Ok(Instruction::Toggle("a".to_owned()))
        );
        assert_eq!(
            Instruction::from_str("out x"),
            Ok(Instruction::Transmit("x".to_owned()))
        );
        assert!(Instruction::from_str("").is_err());
        assert!(Instruction::from_str("abc").is_err());
        assert!(Instruction::from_str("cpy").is_err());
        assert!(Instruction::from_str("cpy 41").is_err());
        assert!(Instruction::from_str("cpy 41 a b").is_err());
    }

    #[test]
    fn test_day12() {
        assert_eq!(
            run_instructions(&collect_from_lines(EXAMPLE_DAY_12), 0, 0),
            42
        );
        assert_eq!(
            run_instructions(&collect_from_lines(EXAMPLE_DAY_12), 0, 1),
            42
        );
    }

    #[test]
    fn test_day23() {
        assert_eq!(
            run_instructions(&collect_from_lines(EXAMPLE_DAY_23), 7, 0),
            3
        );
        assert_eq!(
            run_instructions(&collect_from_lines(EXAMPLE_DAY_23), 12, 0),
            3
        );
    }
}
