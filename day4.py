"""Advent of Code - Day 4"""

import re

def load(fname):
    """Load memory string from file."""
    with open(fname, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

# find "X", search all adjacents for "M". If found, search the same adjacent
# relative to M for "A" and then the same relative to A for "S".

def find_xmas(matrix):
    matches = 0

    # east/west
    for row in matrix:
        matches += len(re.findall(r"XMAS", row))
        matches += len(re.findall(r"SAMX", row))

    # north/south
    txt_northsouth = ""
    for c, char in enumerate(matrix[0]):
        for r, row in enumerate(matrix):
            txt_northsouth += matrix[r][c]
        txt_northsouth += "|" # avoid hits across cols

    matches += len(re.findall(r"XMAS", txt_northsouth))
    matches += len(re.findall(r"SAMX", txt_northsouth))

    # diagonals left to right
    # find each X and S, then look diagonally left and right for XMAS or SAMX
    xs = []
    ss = []
    for r, row in enumerate(matrix):
        for c, char in enumerate(row):
            if matrix[r][c] == "X":
                xs.append((r, c))
            if matrix[r][c] == "S":
                ss.append((r, c))

    cmax = len(matrix[0]) - 1
    rmax = len(matrix) -1

    # look on primary diagonals
    for pos in xs:
        r, c = pos
        if c <= cmax - 3 and r <= rmax - 3:
            if matrix[r+1][c+1] == "M" and matrix[r+2][c+2] == "A" and matrix[r+3][c+3] == "S":
                matches += 1

    for pos in ss:
        r, c = pos
        if c <= cmax - 3 and r <= rmax - 3:
            if matrix[r+1][c+1] == "A" and matrix[r+2][c+2] == "M" and matrix[r+3][c+3] == "X":
                matches += 1

    # look on secondary diagonals
    for pos in xs:
        r, c = pos
        if c >= 3 and r <= rmax - 3:
            if matrix[r+1][c-1] == "M" and matrix[r+2][c-2] == "A" and matrix[r+3][c-3] == "S":
                matches += 1

    for pos in ss:
        r, c = pos
        if c >= 3 and r <= rmax - 3:
            if matrix[r+1][c-1] == "A" and matrix[r+2][c-2] == "M" and matrix[r+3][c-3] == "X":
                matches += 1

    return matches

def find_masmas(matrix):
    rmax = len(matrix) - 1
    cmax = len(matrix) - 1

    xcount = 0

    for r in range(rmax-1):
        for c in range(cmax-1):
            minimatrix = [matrix[r][c:c+3], matrix[r+1][c:c+3], matrix[r+2][c:c+3]]

            # assume only diagonals
            primary_diagonal = minimatrix[0][0]+minimatrix[1][1]+minimatrix[2][2]
            secondary_diagonal = minimatrix[0][2]+minimatrix[1][1]+minimatrix[2][0]

            if primary_diagonal in ["SAM", "MAS"] and secondary_diagonal in ["SAM", "MAS"]:
                xcount += 1

    return xcount


def test_find_xmas():
    matrix = load("data/day4_test.txt")
    assert find_xmas(matrix) == 18

def test_find_masmas():
    matrix = load("data/day4_test.txt")
    assert find_masmas(matrix) == 9


def solve_part1():
    matrix = load("data/day4_data.txt")
    result = find_xmas(matrix)
    print(f"Part 1: {result}")

def solve_part2():
    matrix = load("data/day4_data.txt")
    result = find_masmas(matrix)
    print(f"Part 2: {result}")


if __name__ == "__main__":
    solve_part1()
    solve_part2()