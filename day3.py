"""Advent of Code - Day 3"""

import re

def load(fname):
    """Load memory string from file."""
    with open(fname, "r", encoding="utf-8") as f:
        return f.read().replace("\n", "")

def find_multiply_muls(txt):
    """Find all occurrences of mul(#,#). Multiply them, return the sum."""
    muls = []
    for match in re.findall(r"mul\(\d+,\d+\)", txt):
        muls.append([int(m) for m in match.strip("mul(").strip(")").split(",")])

    return sum([a*b for a, b in muls])

def find_multiply_muls_conditional(txt):
    """Find all occurences of mul(#,#) that are enabled (occur after) a "do()".
    without being disabled (occur after) a "don't()" Start of string is state
    "enabled", i.e. there is a "do()" before the whole string.
    """

    # pattern to find:
    # do() <-- anything but not do() or don't() --> mul(#,#)

    enabledmatches = re.findall(r"do\(\)(?:(?!do\(\)|don't\(\)).)*mul\(\d+,\d+\)", "do()"+txt)
    matches = []
    for enabledmatch in enabledmatches:
        matches += re.findall(r"mul\(\d+,\d+\)", enabledmatch)
    
    muls = []
    for match in matches:
        mul = [int(m) for m in match.strip("mul(").strip(")").split(",")]
        muls.append(mul)

    return sum([a*b for a, b in muls])

def test_find_multiply_muls():
    memory = load("data/day3_test1.txt")
    assert find_multiply_muls(memory) == 161

def test_find_multiply_muls_conditional():
    memory = load("data/day3_test2.txt")
    assert find_multiply_muls_conditional(memory) == 48

def solve_part1():
    memory = load("data/day3_data.txt")
    result = find_multiply_muls(memory)
    print(f"Part 1: {result}")

def solve_part2():
    memory = load("data/day3_data.txt")
    result = find_multiply_muls_conditional(memory)
    print(f"Part 2: {result}")


if __name__ == "__main__":
    solve_part1()
    solve_part2()