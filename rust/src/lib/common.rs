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
            "use std::fs;"
        );
    }
}
