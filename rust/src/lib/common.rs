// First line
use std::borrow::ToOwned;
use std::fs;

#[must_use]
pub fn get_first_line(string: &str) -> String {
    match string.lines().next() {
        None => "",
        Some(l) => l,
    }
    .to_string()
}

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
pub fn collect_from_lines<Item, F, E>(string: &str, f: F) -> Vec<Item>
where
    F: Fn(&str) -> Result<Item, E>,
    E: std::fmt::Debug,
{
    string.lines().map(|l| f(l).unwrap()).collect()
}

pub mod point_module {
    #[derive(Debug, PartialEq, Eq, Hash)]
    pub struct Point<T> {
        pub x: T,
        pub y: T,
    }

    #[derive(Debug, PartialEq, Eq, Hash)]
    pub struct FromStrError;

    use std::str::FromStr;
    impl<T: std::str::FromStr> Point<T> {
        #[allow(clippy::result_unit_err, clippy::missing_errors_doc)]
        pub fn from_str_with_param(s: &str, separator: &str) -> Result<Self, FromStrError> {
            let (x, y) = s.split_once(separator).ok_or(FromStrError)?;
            Ok(Self {
                x: x.parse().map_err(|_| FromStrError)?,
                y: y.parse().map_err(|_| FromStrError)?,
            })
        }
    }

    impl<T: std::str::FromStr> FromStr for Point<T> {
        type Err = ();
        fn from_str(s: &str) -> Result<Self, Self::Err> {
            let (x, y) = s.split_once(", ").ok_or(())?;
            Ok(Self {
                x: x.parse().map_err(|_| {})?,
                y: y.parse().map_err(|_| {})?,
            })
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::point_module::Point;
    use std::str::FromStr;

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
}
