"""Advent of Code - Day 7"""

import itertools
from time import time


def load(fname):

    equations = {}
    with open(fname, "r", encoding="utf-8") as f:
        for line in f.readlines():
            eq, num = line.split(":")
            equations[int(eq)] = [int(n) for n in num.strip().split()]

    return equations


def find_all_valid_expressions(equations, operators):
    """Given a sequence of numbers, return all possible combinations."""
    # valids = {1: [1, 2, 3], 2: [1, 2, 3]}

    keys_of_valids = []

    for value, numbers in equations.items():

        # Make all possible expressions
        operator_combinations = list(
            itertools.product(operators, repeat=len(numbers) - 1)
        )

        for operator_combination in operator_combinations:
            if evaluate(numbers, list(operator_combination)) == value:
                keys_of_valids.append(value)
                break  # only care about the first

    return keys_of_valids


def evaluate(numbers, operators: list):
    """Evaluate expression left to right."""

    result = numbers[0]

    for operator, number in zip(operators, numbers[1:]):
        if operator == "+":
            result += number
        elif operator == "*":
            result *= number
        elif operator == "||":
            result = int(str(result) + str(number))
        else:
            raise ValueError(f"Uknown operator: {operator}")

    return result


def test_evaluate():
    assert evaluate([1, 2, 3], ["+", "+"]) == 6
    assert evaluate([1, 2, 3], ["+", "*"]) == 9
    assert evaluate([1, 2, 3], ["*", "*"]) == 6
    assert evaluate([2, 3, 4], ["*", "+"]) == 10
    assert evaluate([81, 40, 27], ["+", "*"]) == 3267
    assert evaluate([81, 40, 27], ["*", "+"]) == 3267
    assert evaluate([15, 6], ["||"]) == 156
    assert evaluate([6, 8, 6, 15], ["*", "||", "*"]) == 7290
    assert evaluate([17, 8, 14], ["||", "+"]) == 192
    assert evaluate([1, 2, 3], ["||", "+"]) == 15
    assert evaluate([1, 2, 3], ["||", "||"]) == 123
    assert evaluate([1, 2, 3], ["+", "||"]) == 33


def test_find_all_valid_expressions():
    equations = load("data/day7_test.txt")

    # Part 1
    keys_of_valids = find_all_valid_expressions(equations, ["+", "*"])

    assert len(keys_of_valids) == 3
    assert sorted(keys_of_valids) == [190, 292, 3267]
    assert sum(keys_of_valids) == 3749, sum(keys_of_valids)

    # Part 2
    keys_of_valids_concat = find_all_valid_expressions(equations, ["+", "*", "||"])

    assert len(keys_of_valids_concat) == 6
    assert sum(keys_of_valids_concat) == 11387


def solve_part1():
    equations = load("data/day7_data.txt")
    start = time()
    keys_of_valids = find_all_valid_expressions(equations, ["+", "*"])
    elapsed = time() - start
    result = sum(keys_of_valids)
    print(f"Part 1: {result} ({round(elapsed,2)} s)")


def solve_part2():
    equations = load("data/day7_data.txt")
    start = time()
    keys_of_valids = find_all_valid_expressions(equations, ["+", "*", "||"])
    elapsed = time() - start
    result = sum(keys_of_valids)
    print(f"Part 2: {result} ({round(elapsed,2)} s)")


if __name__ == "__main__":
    solve_part1()
    solve_part2()
