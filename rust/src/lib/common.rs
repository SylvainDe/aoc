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

#[cfg(test)]
mod tests {
    use super::*;

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
