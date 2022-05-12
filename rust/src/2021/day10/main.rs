use std::fs;

const INPUT_FILEPATH: &str = "res/2021/day10/input.txt";

type Int = u32;
type InputContent = Vec<String>;

fn get_input_from_str(string: &str) -> InputContent {
    string.lines().map(|l| l.to_string()).collect()
}

fn get_input_from_file(filepath: &str) -> InputContent {
    get_input_from_str(&fs::read_to_string(filepath).expect("Could not open file"))
}

#[derive(Debug, PartialEq)]
enum ParseResult {
    Success,
    Corrupted(char),
    // Incomplete,
}

fn parse_string(s: &str) -> ParseResult {
    let mut stack: Vec<char> = Vec::new();
    for c in s.chars() {
        match c {
            '(' => stack.push(')'),
            '{' => stack.push('}'),
            '[' => stack.push(']'),
            '<' => stack.push('>'),
            _ => match stack.pop() {
                None => return ParseResult::Corrupted(c),
                Some(expected) => {
                    if expected != c {
                        return ParseResult::Corrupted(c);
                    }
                }
            },
        }
    }
    ParseResult::Success
}

fn syntax_error_score(s: &str) -> Int {
    match parse_string(s) {
        ParseResult::Corrupted(c) => match c {
            ')' => 3,
            ']' => 57,
            '}' => 1197,
            '>' => 25137,
            _ => panic!("Unexpected value {}", c),
        },
        _ => 0,
    }
}

fn part1(strings: &InputContent) -> Int {
    strings.iter().map(|s| syntax_error_score(s)).sum()
}

fn part2(_arg: &InputContent) -> Int {
    0
}

fn main() {
    let strings = get_input_from_file(INPUT_FILEPATH);
    let res = part1(&strings);
    println!("{:?}", res);
    assert_eq!(res, 339411);
    let res2 = part2(&strings);
    println!("{:?}", res2);
    assert_eq!(res2, 0);
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE: &str = "[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]";

    #[test]
    fn test_parse_legal_string() {
        assert_eq!(parse_string("()"), ParseResult::Success);
        assert_eq!(parse_string("[]"), ParseResult::Success);
        assert_eq!(parse_string("([])"), ParseResult::Success);
        assert_eq!(parse_string("{()()()}"), ParseResult::Success);
        assert_eq!(parse_string("<([{}])>"), ParseResult::Success);
        assert_eq!(parse_string("[<>({}){}[([])<>]]"), ParseResult::Success);
        assert_eq!(parse_string("(((((((((())))))))))"), ParseResult::Success);
    }

    #[test]
    fn test_parse_corrupted_string() {
        assert_eq!(parse_string("(]"), ParseResult::Corrupted(']'));
        assert_eq!(parse_string("{()()()>"), ParseResult::Corrupted('>'));
        assert_eq!(parse_string("(((()))}"), ParseResult::Corrupted('}'));
        assert_eq!(parse_string("<([]){()}[{}])"), ParseResult::Corrupted(')'));
        //- Expected ], but found } instead.
        assert_eq!(
            parse_string("{([(<{}[<>[]}>{[]{[(<()>"),
            ParseResult::Corrupted('}')
        );
        // Expected ], but found ) instead.
        assert_eq!(
            parse_string("[[<[([]))<([[{}[[()]]]"),
            ParseResult::Corrupted(')')
        );
        // Expected ), but found ] instead.
        assert_eq!(
            parse_string("[{[{({}]{}}([{[{{{}}([]"),
            ParseResult::Corrupted(']')
        );
        // Expected >, but found ) instead.
        assert_eq!(
            parse_string("[<(<(<(<{}))><([]([]()"),
            ParseResult::Corrupted(')')
        );
        // Expected ], but found > instead
        assert_eq!(
            parse_string("<{([([[(<>()){}]>(<<{{"),
            ParseResult::Corrupted('>')
        );
    }

    #[test]
    fn test_parse_strings_example() {
        for s in get_input_from_str(EXAMPLE) {
            // Nothing is checked yet
            parse_string(&s);
        }
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 26397);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 0);
    }
}
