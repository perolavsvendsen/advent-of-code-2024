"""Advent of Code - Day 1"""


def load(fname):
    lefts = []
    rights = []

    with open(fname, "r", encoding="utf-8") as f:
        for line in f.readlines():
            (l, r) = tuple(line.split())
            lefts.append(l)
            rights.append(r)

    return sorted([int(l) for l in lefts]), sorted([int(r) for r in rights])


def calculate_dists(lefts, rights):
    """Calculate (absolute) distance between each number in the sorted list."""
    dists = []
    while lefts:
        dists.append(abs(rights.pop(0) - lefts.pop(0)))
    return dists


def test_part1():
    lefts, rights = load("day1/data_test.txt")
    dists = calculate_dists(lefts, rights)
    assert dists == [2, 1, 0, 1, 2, 5]  # sum = 11


def solve_part1():
    lefts, rights = load("day1/data_1.txt")
    print(f"Part 1: {sum(calculate_dists(lefts, rights))}")


def calculate_similarity_score(lefts, rights):
    """Calculate a total similarity score by adding up each number in the left
    list after multiplying it by the number of times that number appears in the
    right list."""

    similarity_score = 0
    for item in lefts:
        similarity_score += item * rights.count(item)

    return similarity_score


def test_part2():
    lefts, rights = load("day1/data_test.txt")
    similarity_score = calculate_similarity_score(lefts, rights)
    assert similarity_score == 31


def solve_part2():
    lefts, rights = load("day1/data_1.txt")
    similarity_score = calculate_similarity_score(lefts, rights)
    print(f"Part 2: {similarity_score}")


if __name__ == "__main__":
    solve_part1()
    solve_part2()
