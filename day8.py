"""Advent of Code - Day 8"""

import itertools


def load(fname):
    """Parse from file."""
    with open(fname, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]


def find_unique_frequencies(map_):
    """Return all unique frequencies in map_."""
    return set([item for row in map_ for item in row if item != "."])


def test_find_unique_frequencies():
    map_ = load("data/day8_test.txt")
    assert sorted(find_unique_frequencies(map_)) == sorted(["A", "0"])


def find_antennas(map_, freq):
    """Return positions for all antennas on freq in map_."""
    all_antennas = []
    for r, _ in enumerate(map_):
        for c, _ in enumerate(map_[0]):
            if map_[r][c] == freq:
                all_antennas.append((r, c))

    return all_antennas


def test_find_antennas():
    map_ = load("data/day8_test.txt")
    assert find_antennas(map_, "0") == [(1, 8), (2, 5), (3, 7), (4, 4)]


def find_antinodes(map_, pair):
    """Return valid antinode positions for this pair on this map_."""

    rmax = len(map_) - 1
    cmax = len(map_[0]) - 1

    (r1, c1), (r2, c2) = pair

    dr, dc = (r1 - r2, c1 - c2)

    a1 = (r1 + dr, c1 + dc)
    a2 = (r2 - dr, c2 - dc)

    antinodes = []

    for ar, ac in [a1, a2]:
        if 0 <= ar <= rmax and 0 <= ac <= cmax:
            antinodes.append((ar, ac))

    return antinodes


def test_find_antinodes():
    map_ = load("data/day8_test.txt")

    assert find_antinodes(map_, ((3, 4), (5, 5))) == [(1, 3), (7, 6)]
    assert find_antinodes(map_, ((0, 1), (0, 3))) == [(0, 5)]
    assert find_antinodes(map_, ((0, 0), (3, 0))) == [(6, 0)]
    assert find_antinodes(map_, ((11, 0), (0, 11))) == []
    assert find_antinodes(map_, ((5, 5), (7, 7))) == [(3, 3), (9, 9)]
    assert find_antinodes(map_, ((7, 7), (5, 5))) == [(9, 9), (3, 3)]
    assert sorted(find_antinodes(map_, ((5, 7), (7, 5)))) == sorted([(9, 3), (3, 9)])


def find_antinodes_repeating(map_, pair):
    """Return all valid repeating antinode positions for this pair, on this
    map_."""

    rmax = len(map_) - 1
    cmax = len(map_[0]) - 1

    (r1, c1), (r2, c2) = pair

    antinodes = [(r1, c1), (r2, c2)]  # also include antenna positions

    def inside(map_, pos):
        r, c = pos
        return 0 <= r <= rmax and 0 <= c <= cmax

    dr, dc = (r1 - r2, c1 - c2)  # continue this diff in all directions

    while True:
        antinode = (r1 + dr, c1 + dc)
        if not inside(map_, antinode):
            break
        antinodes.append(antinode)
        r1, c1 = antinode

    while True:
        antinode = (r1 - dr, c1 - dc)
        if not inside(map_, antinode):
            break
        antinodes.append(antinode)
        r1, c1 = antinode

    antinodes = list(set(sorted(antinodes)))

    return antinodes


def test_find_antinodes_repeating():
    map_ = load("data/day8_test.txt")

    assert sorted(find_antinodes_repeating(map_, ((3, 5), (5, 5)))) == sorted(
        [
            (1, 5),
            (3, 5),
            (5, 5),
            (7, 5),
            (9, 5),
            (11, 5),
        ]
    )


def test_find_all_antinodes():
    map_ = load("data/day8_test.txt")
    assert len(find_all_antinodes(map_)) == 14


def find_all_antinodes(map_, repeating=False):
    """Return all unique antinodes for all antennas on this map_."""

    unique_freq = find_unique_frequencies(map_)

    # find all pairs of each frequency
    antinodes = []
    for freq in unique_freq:
        antennas = find_antennas(map_, freq)

        antenna_pairs = list(itertools.combinations(antennas, 2))

        # for each pair, find antinodes that are inside map
        for pair in antenna_pairs:
            if repeating:
                antinodes += find_antinodes_repeating(map_, pair)
            else:
                antinodes += find_antinodes(map_, pair)

    return set(antinodes)


def test_find_all_antinodes_repeating():
    map_ = load("data/day8_test.txt")
    assert len(find_all_antinodes(map_, repeating=True)) == 34


def solve_part1():
    map_ = load("data/day8_data.txt")
    result = len(find_all_antinodes(map_))
    print(f"Part 1: {result}")


def solve_part2():
    map_ = load("data/day8_data.txt")
    result = len(find_all_antinodes(map_, repeating=True))
    print(f"Part 2: {result}")


if __name__ == "__main__":
    solve_part1()
    solve_part2()
