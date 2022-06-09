#[must_use]
pub fn get_first_line(string: &str) -> String {
    match string.lines().next() {
        None => "",
        Some(l) => l,
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
