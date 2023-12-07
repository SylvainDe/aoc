# vi: set shiftwidth=4 tabstop=4 expandtab:
import datetime
import os
import math
import functools
import collections


top_dir = os.path.dirname(os.path.abspath(__file__)) + "/../../"

def get_orders_from_file(file_path=top_dir + "resources/year2019_day22_input.txt"):
    with open(file_path) as f:
        return [l.strip() for l in f]


# Note: Many functions here are basic implementations
# which are mostly used to provide results that are
# easy to check. These results can then be used to
# test trickier and trickier implementations:
#  - implement operations on the whole deck
#  - implement operations to track a single card
#  - implement operations to track a card in reverse
#  - optimise the single-card operations using some
#     modular trickery.
# For the final result, one can directly skip to the
# function apply_modular_orders.


# Basic operations on full deck
def new_deck(nb):
    return list(range(nb))


def deal_into_new_stack(deck):
    return list(reversed(deck))


def cut_n_cards(deck, n):
    left, right = deck[:n], deck[n:]
    return right + left


def deal_with_increment(deck, n):
    l = len(deck)
    assert math.gcd(l, n) == 1
    deck2 = [0] * l
    for i in range(l):
        deck2[(n * i) % l] = deck[i]
    return deck2


# Basic operations on single card
def single_deal_into_new_stack(nb_cards, position):
    return (-position - 1) % nb_cards


def single_cut_n_cards(nb_cards, n, position):
    return (position - n) % nb_cards


def single_deal_with_increment(nb_cards, n, position):
    return (n * position) % nb_cards


# Basic operation on single cards described as modular operation
def modular_deal_into_new_stack():
    return (-1, -1)


def modular_cut_into_n_card(n):
    return (1, -n)


def modular_deal_with_increment(n):
    return (n, 0)


# Reverse operation on single card
def reverse_deal_into_new_stack(nb_cards, position):
    """Same as single_deal_into_new_stack."""
    return (-position - 1) % nb_cards


def reverse_cut_n_cards(nb_cards, n, position):
    """Same as single_cut_n_cards with reversed argument."""
    return (position + n) % nb_cards


def reverse_deal_with_increment(nb_cards, n, position):
    assert math.gcd(nb_cards, n) == 1
    # Card i ends up at position j such that: j = (n*i) % nb_cards
    # Finding i from j corresponds to finding the inverse of n modulo nb_cards
    return (position * modinv(n, nb_cards)) % nb_cards


def xgcd(a, b):
    """Computes the extended gcd."""
    # http://anh.cs.luc.edu/331/notes/xgcd.pdf
    prevx, x = 1, 0
    prevy, y = 0, 1
    while b:
        q = a // b
        x, prevx = prevx - q * x, x
        y, prevy = prevy - q * y, y
        a, b = b, a % b
    return a, prevx, prevy


@functools.lru_cache()
def modinv(a, m):
    """Computes the Modular multiplicative inverse."""
    g, x, _ = xgcd(a, m)
    if g != 1:
        raise Exception("modular inverse does not exist")
    return x % m


# Orders
Operation = collections.namedtuple(
    "Operation", ["deck", "single", "reverse", "modular"]
)
orders = {
    "deal into new stack": Operation(
        deal_into_new_stack,
        single_deal_into_new_stack,
        reverse_deal_into_new_stack,
        modular_deal_into_new_stack,
    ),
    "cut ": Operation(
        cut_n_cards, single_cut_n_cards, reverse_cut_n_cards, modular_cut_into_n_card
    ),
    "deal with increment ": Operation(
        deal_with_increment,
        single_deal_with_increment,
        reverse_deal_with_increment,
        modular_deal_with_increment,
    ),
}


def get_order_and_remaining(order):
    for prefix, op in orders.items():
        if order.startswith(prefix):
            return op, order[len(prefix) :]
    assert False


# Orders on the whole deck
def apply_order(order, deck):
    op, rem = get_order_and_remaining(order)
    return op.deck(deck, int(rem)) if rem else op.deck(deck)


def apply_orders(nb, orders, repetition=1):
    deck = new_deck(nb)
    for _ in range(repetition):
        for order in orders:
            deck = apply_order(order, deck)
    return deck


# Orders on single cards
def apply_single_order(order, nb_cards, position):
    op, rem = get_order_and_remaining(order)
    return op.single(nb_cards, int(rem), position) \
           if rem else \
           op.single(nb_cards, position)


def apply_single_orders(orders, nb_cards, position):
    for order in orders:
        position = apply_single_order(order, nb_cards, position)
    return position


# Reverse orders on single cards
def apply_reverse_order(order, nb_cards, position):
    op, rem = get_order_and_remaining(order)
    return op.reverse(nb_cards, int(rem), position) \
           if rem else \
           op.reverse(nb_cards, position)


def apply_reverse_orders(orders, nb_cards, position):
    for order in reversed(orders):
        position = apply_reverse_order(order, nb_cards, position)
    return position


# Orders on single cards using modular logic
# All orders can be seen as computing
#   pos2 = (pos1 * A1 + b1) % nb_cards
# And they can be combined as such
#
#   pos3 = (pos2 * A2 + b2) % nb_cards
#        = ((pos1 * A1 + b1) * A2 + b2) % nb_cards
#        = (pos1 * A1 * A2 + b1 * A2 + b2) % nb_cards
#                  ~~~~~~~   ~~~~~~~~~~~~
#                    ~A~          ~B~
#
# Hence, we can summarize an order but also a list of orders
# as a tuple (a, b):
#  - it can be applied very efficiently
#  - it can be applied in reverse very efficiently too
#  - it can be applied multiple times very efficiently
def get_modular_param(orders, repetition, nb_cards):
    a, b = 1, 0
    for order in orders:
        op, rem = get_order_and_remaining(order)
        curr_a, curr_b = op.modular(int(rem)) if rem else op.modular()
        a = a * curr_a % nb_cards
        b = b * curr_a + curr_b % nb_cards
    # All orders are summarised as (a, b)
    if repetition == 1:
        return a, b
    # Repetitions can then be computed with exponentiation
    #  a, a^2, a^3.. a^n
    #  b, b*(a+1), b*(a^2 + a + 1), b*(a^n+...+a^3+a^2+a+1) = b*(a^(n+1) - 1)/(a - 1)
    sum_a = (pow(a, repetition) - 1) // (a - 1)
    a = pow(a, repetition)
    return a, sum_a * b


def apply_modular_orders(orders, nb_cards, position, repetition=1):
    a, b = get_modular_param(orders, repetition, nb_cards)
    return (a * position + b) % nb_cards


def apply_modular_reversed_orders(orders, nb_cards, position, repetition=1):
    # We have the property:
    #   pos2 = (pos1 * a + b) % nb_cards
    # And we want to compute pos1 from a, b, pos2 and nb_cards
    #   (pos2 - b) = pos1 * a % nb_cards
    # We must find the inverse of a modulo nb_cards
    a, b = get_modular_param(orders, repetition, nb_cards)
    return ((position - b) * modinv(a, nb_cards)) % nb_cards


# Tests
def test_minimal_operations():
    deck = new_deck(10)
    assert deck == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert deal_into_new_stack(deck) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert cut_n_cards(deck, 3) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert cut_n_cards(deck, -4) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    assert deal_with_increment(deck, 3) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
    assert deck == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_single_card_operations():
    for nb_cards in [10, 20]:
        deck = deal_into_new_stack(new_deck(nb_cards))
        for pos, card in enumerate(deck):
            assert single_deal_into_new_stack(nb_cards, card) == pos
            assert reverse_deal_into_new_stack(nb_cards, pos) == card
            a, b = modular_deal_into_new_stack()
            assert (a * card + b) % nb_cards == pos
        for cut_arg in [3, -4]:
            deck = cut_n_cards(new_deck(nb_cards), cut_arg)
            a, b = modular_cut_into_n_card(cut_arg)
            for pos, card in enumerate(deck):
                assert single_cut_n_cards(nb_cards, cut_arg, card) == pos
                assert reverse_cut_n_cards(nb_cards, cut_arg, pos) == card
                assert (a * card + b) % nb_cards == pos
        for incr_arg in [3]:
            deck = deal_with_increment(new_deck(nb_cards), incr_arg)
            a, b = modular_deal_with_increment(incr_arg)
            for pos, card in enumerate(deck):
                assert single_deal_with_increment(nb_cards, incr_arg, card) == pos
                assert reverse_deal_with_increment(nb_cards, incr_arg, pos) == card
                assert (a * card + b) % nb_cards == pos


def test_single_card_orders(nb_cards, orders):
    # Test that single card operation tracks every card properly
    result = apply_orders(nb_cards, orders)
    for pos, card in enumerate(result):
        assert apply_single_orders(orders, nb_cards, card) == pos
        assert apply_modular_orders(orders, nb_cards, card) == pos
        assert apply_reverse_orders(orders, nb_cards, pos) == card
        assert apply_modular_reversed_orders(orders, nb_cards, pos) == card
    # Test that repetitions of orders can be tracked
    result2 = apply_orders(nb_cards, orders, 2)
    for pos2, card2 in enumerate(result2):
        pos1 = result.index(card2)
        # Test with temporary positions
        assert apply_single_orders(orders, nb_cards, pos1) == pos2
        assert apply_modular_orders(orders, nb_cards, pos1) == pos2
        assert apply_reverse_orders(orders, nb_cards, pos2) == pos1
        assert apply_modular_reversed_orders(orders, nb_cards, pos2) == pos1
        # Test with a single operation
        assert apply_modular_orders(orders, nb_cards, card2, 2) == pos2
        assert apply_modular_reversed_orders(orders, nb_cards, pos2, 2) == card2
    # More iterations to be sure
    for rep in [1, 2, 5, 20]:
        result = apply_orders(nb_cards, orders, rep)
        for pos, card in enumerate(result):
            assert apply_modular_orders(orders, nb_cards, card, rep) == pos
            assert apply_modular_reversed_orders(orders, nb_cards, pos, rep) == card


def test_orders():
    nb_cards = 10
    orders = [
        "deal with increment 7",
        "deal into new stack",
        "deal into new stack",
    ]
    assert apply_orders(nb_cards, orders) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
    test_single_card_orders(nb_cards, orders)
    orders = [
        "cut 6",
        "deal with increment 7",
        "deal into new stack",
    ]
    assert apply_orders(nb_cards, orders) == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
    test_single_card_orders(nb_cards, orders)
    orders = [
        "deal with increment 7",
        "deal with increment 9",
        "cut -2",
    ]
    assert apply_orders(nb_cards, orders) == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]
    test_single_card_orders(nb_cards, orders)
    orders = [
        "deal into new stack",
        "cut -2",
        "deal with increment 7",
        "cut 8",
        "cut -4",
        "deal with increment 7",
        "cut 3",
        "deal with increment 9",
        "deal with increment 3",
        "cut -1",
    ]
    assert apply_orders(nb_cards, orders) == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]
    test_single_card_orders(nb_cards, orders)


def run_tests():
    test_minimal_operations()
    test_single_card_operations()
    test_orders()


def part1(orders):
    nb_cards = 10007
    card_number = 2019
    return apply_modular_orders(orders, nb_cards, card_number)


def part2(orders):
    nb_cards = 119315717514047
    final_position = 2020
    nb_shuffle = 101741582076661
    return apply_modular_reversed_orders(orders, nb_cards, final_position, nb_shuffle)


def get_solutions():
    orders = get_orders_from_file()
    print(part1(orders) == 7860)
    # print(part2(orders)) - not fast enough >_<


if __name__ == "__main__":
    begin = datetime.datetime.now()
    run_tests()
    get_solutions()
    end = datetime.datetime.now()
    print(end - begin)
