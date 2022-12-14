use common::input::collect_lines;
use common::input::get_file_content;
use std::time::Instant;

const INPUT_FILEPATH: &str = "../resources/year2021_day10_input.txt";

type Int = u64;
type InputContent = Vec<String>;

fn get_input_from_str(string: &str) -> InputContent {
    collect_lines(string)
}

#[derive(Debug, PartialEq)]
enum ParseResult {
    Success,
    Corrupted(char),
    Incomplete(String),
}

fn parse_string(s: &str) -> ParseResult {
    let mut stack = Vec::new();
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
    if stack.is_empty() {
        ParseResult::Success
    } else {
        ParseResult::Incomplete(stack.into_iter().rev().collect())
    }
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
        ParseResult::Success | ParseResult::Incomplete(_) => 0,
    }
}

fn part1(strings: &InputContent) -> Int {
    strings.iter().map(|s| syntax_error_score(s)).sum()
}

fn completion_score_for_missing(s: &str) -> Int {
    let mut score: Int = 0;
    for c in s.chars() {
        score *= 5;
        score += match c {
            ')' => 1,
            ']' => 2,
            '}' => 3,
            '>' => 4,
            _ => panic!("Unexpected value {}", c),
        }
    }
    score
}

fn completion_score(s: &str) -> Int {
    match parse_string(s) {
        ParseResult::Incomplete(missing) => completion_score_for_missing(&missing),
        ParseResult::Success | ParseResult::Corrupted(_) => 0,
    }
}

fn part2(strings: &InputContent) -> Int {
    let mut values: Vec<Int> = strings
        .iter()
        .map(|s| completion_score(s))
        .filter(|n| *n > 0)
        .collect();
    values.sort_unstable();
    let n = (values.len() - 1) / 2;
    values[n]
}

fn main() {
    let before = Instant::now();
    let strings = get_input_from_str(&get_file_content(INPUT_FILEPATH));
    let res = part1(&strings);
    println!("{:?}", res);
    assert_eq!(res, 339_411);
    let res2 = part2(&strings);
    println!("{:?}", res2);
    assert_eq!(res2, 2_289_754_624);
    println!("Elapsed time: {:.2?}", before.elapsed());
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
    fn test_parse_incomplete_string() {
        // Complete by adding }}]])})]
        assert_eq!(
            parse_string("[({(<(())[]>[[{[]{<()<>>"),
            ParseResult::Incomplete("}}]])})]".to_owned())
        );
        // Complete by adding )}>]})
        assert_eq!(
            parse_string("[(()[<>])]({[<{<<[]>>("),
            ParseResult::Incomplete(")}>]})".to_owned())
        );
        // Complete by adding }}>}>))))
        assert_eq!(
            parse_string("(((({<>}<{<{<>}{[]{[]{}"),
            ParseResult::Incomplete("}}>}>))))".to_owned())
        );
        // Complete by adding ]]}}]}]}>
        assert_eq!(
            parse_string("{<[[]]>}<{[{[{[]{()[[[]"),
            ParseResult::Incomplete("]]}}]}]}>".to_owned())
        );
        // Complete by adding ])}>
        assert_eq!(
            parse_string("<{([{{}}[<[[[<>{}]]]>[]]"),
            ParseResult::Incomplete("])}>".to_owned())
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
    fn test_completion_score_for_missing() {
        assert_eq!(completion_score_for_missing("}}]])})]"), 288_957);
        assert_eq!(completion_score_for_missing(")}>]})"), 5566);
        assert_eq!(completion_score_for_missing("}}>}>))))"), 1_480_781);
        assert_eq!(completion_score_for_missing("]]}}]}]}>"), 995_444);
        assert_eq!(completion_score_for_missing("])}>"), 294);
    }

    #[test]
    fn test_part1() {
        assert_eq!(part1(&get_input_from_str(EXAMPLE)), 26397);
    }

    #[test]
    fn test_part2() {
        assert_eq!(part2(&get_input_from_str(EXAMPLE)), 288_957);
    }
}
