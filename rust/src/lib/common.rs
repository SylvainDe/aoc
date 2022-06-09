#[allow(clippy::missing_panics_doc)]
#[must_use]
pub fn get_first_line(string: &str) -> String {
    if string.is_empty() {
        ""
    } else {
        let mut line_it = string.lines();
        line_it.next().unwrap()
    }
    .to_string()
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
}
