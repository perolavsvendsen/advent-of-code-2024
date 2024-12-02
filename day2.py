"""Advent of Code - Day 1"""


def load(fname):
    """Load reports from file, one per line."""
    reports = []
    with open(fname, "r", encoding="utf-8") as f:
        for line in f.readlines():
            report = [int(x) for x in line.split()]
            reports.append(report)
    return reports


def is_safe(report):
    """Return True if report is Safe:
    - All increasing or decreasing
    - All levels differ by at least one or at most 3
    """

    pairs = [pair for pair in zip(report, report[1:])]
    return (all([a < b for a, b in pairs]) or all([a > b for a, b in pairs])) and (
        all([1 <= abs(a - b) <= 3 for a, b in pairs])
    )


def is_safe_dampener(report):
    """Return True if report is Safe:
    - All increasing or decreasing
    - All levels differ by at least one or at most 3
    - If removing a single level will make it safe
    """

    if is_safe(report) is True:
        return True

    # remove one by one to check if it can be made safe by removing single
    for i, item in enumerate(report):
        newlist = report.copy()
        newlist.pop(i)
        if is_safe(newlist) is True:
            return True

    return False


def test_part1():
    assert is_safe([7, 6, 4, 2, 1]) is True
    assert is_safe([1, 2, 7, 8, 9]) is False
    assert is_safe([9, 7, 6, 2, 1]) is False
    assert is_safe([1, 3, 2, 4, 5]) is False
    assert is_safe([8, 6, 4, 4, 1]) is False
    assert is_safe([1, 3, 6, 7, 9]) is True


def test_part2():
    assert is_safe_dampener([7, 6, 4, 2, 1]) is True
    assert is_safe_dampener([1, 2, 7, 8, 9]) is False
    assert is_safe_dampener([9, 7, 6, 2, 1]) is False
    assert is_safe_dampener([1, 3, 2, 4, 5]) is True
    assert is_safe_dampener([8, 6, 4, 4, 1]) is True
    assert is_safe_dampener([1, 3, 6, 7, 9]) is True


def solve_part1():
    """Solve part 1."""
    reports = load("data/day2_data.txt")
    print(f"Part 1: {sum([is_safe(report) for report in reports])}")


def solve_part2():
    """Solve part 2."""
    reports = load("data/day2_data.txt")
    print(f"Part 2: {sum([is_safe_dampener(report) for report in reports])}")


if __name__ == "__main__":
    solve_part1()
    solve_part2()
