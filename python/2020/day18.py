# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import operator


def get_expr_from_file(file_path="day18_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


def handle_parenthesis(expr, eval_func):
    i = expr.find("(")
    if i == -1:
        return expr
    lhs, rhs = expr[:i], expr[i + 1 :]
    nb_parenth = 1
    for j, c2 in enumerate(rhs):
        if c2 == "(":
            nb_parenth += 1
        elif c2 == ")":
            nb_parenth -= 1
            if nb_parenth == 0:
                inside, rem = rhs[:j], rhs[j + 1 :]
                return lhs + str(eval_func(inside)) + handle_parenthesis(rem, eval_func)
    raise ValueError("Unmatched parenthesis in %s" % expr)


operations = {
    "*": operator.mul,
    "+": operator.add,
    "-": operator.sub,  # Not useful
}


def eval_expr(expr):
    if not expr:
        return 0
    expr = handle_parenthesis(expr, eval_expr)
    # Start from the right to apply operations from left to right
    for i, c in reversed(list(enumerate(expr))):
        op = operations.get(c, None)
        if op is not None:
            lhs, rhs = expr[:i], int(expr[i + 1 :])
            return op(eval_expr(lhs), rhs)
    return int(expr)


def handle_op(expr, eval_func, op, op_func):
    i = expr.find(op)
    if i == -1:
        return expr
    lhs, rhs = expr[:i], expr[i + 1 :]
    return str(op_func(eval_func(lhs), eval_func(rhs)))


def eval_expr2(expr):
    if not expr:
        return 0
    expr = handle_parenthesis(expr, eval_expr2)
    # '*' is handled "first" so that "+" is computed with a higher precedence
    expr = handle_op(expr, eval_expr2, "*", operator.mul)
    expr = handle_op(expr, eval_expr2, "+", operator.add)
    expr = handle_op(expr, eval_expr2, "-", operator.sub)  # Not useful
    return int(expr)


def run_tests():
    # My tests
    assert eval_expr("2 + 3") == 5
    assert eval_expr("2 * 3") == 6
    assert eval_expr("3 - 2") == 1
    assert eval_expr("+2") == 2
    assert eval_expr("-3") == -3
    assert eval_expr("(2)") == 2
    assert eval_expr("((((2))))") == 2
    assert eval_expr("1 + 2 * 3") == 9
    # Tests provided
    assert eval_expr("1 + 2 * 3 + 4 * 5 + 6") == 71
    assert eval_expr("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert eval_expr("2 * 3 + (4 * 5)") == 26
    assert eval_expr("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
    assert eval_expr("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
    assert eval_expr("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632
    # My tests
    assert eval_expr2("2 + 3") == 5
    assert eval_expr2("2 * 3") == 6
    assert eval_expr2("3 - 2") == 1
    assert eval_expr2("+2") == 2
    assert eval_expr2("-3") == -3
    assert eval_expr2("(2)") == 2
    assert eval_expr2("((((2))))") == 2
    assert eval_expr2("1 + 2 * 3") == 9
    assert eval_expr2("1 - 2 + 3") in (-4, 2)  # Evaluation order matters

    assert eval_expr2("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert eval_expr2("2 * 3 + (4 * 5)") == 46
    assert eval_expr2("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
    assert eval_expr2("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
    assert eval_expr2("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340


def get_solutions():
    expr = get_expr_from_file()
    print(sum(eval_expr(e) for e in expr) == 53660285675207)
    print(sum(eval_expr2(e) for e in expr) == 141993988282687)


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
