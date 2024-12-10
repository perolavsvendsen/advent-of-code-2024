"""Advent of Code - Day 10"""


def load(fname):
    with open(fname, "r", encoding="utf-8") as f:
        return [[int(c) for c in line.strip()] for line in f.readlines()]


def find_trails(grid, distinct=False):

    que = []

    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            pos = (r, c)
            value = grid[r][c]
            if value == 0:
                que.append([[pos, value]])

    valid_trails = []
    trailheads = []

    while que:
        current_trail = que.pop(0)

        pos, height = current_trail[-1]  # current position

        if height == 9:
            valid_trails.append(current_trail)
            if current_trail[0] not in trailheads:
                trailheads.append(current_trail[0])
            continue

        nexts = find_neighbors(grid, pos)

        if nexts:
            for next_ in nexts:
                pos, next_height = next_
                if next_height == (height + 1):
                    newtrail = current_trail + [next_]
                    que.append(newtrail)

    if distinct:
        # Accidently seem to have solved part 2 first. Stopping short here will
        # return the solution of part 2.
        return valid_trails, trailheads

    # valid_trails contain lots of trails that start and end at the same
    # places, but the instructions say "how many 9 from each trailhead", so
    # remove those with this pile of duct tape:
    keepers = []
    for trailhead in trailheads:
        reached_peaks = []
        for trail in [t for t in valid_trails if t[0] == trailhead]:
            peak = trail[-1]
            if peak in reached_peaks:
                continue
            else:
                keepers.append(trail)
                reached_peaks.append(peak)

    return keepers, trailheads


def find_neighbors(grid, pos):
    r, c = pos

    rmax = len(grid) - 1
    cmax = len(grid[0]) - 1

    neighbors = []

    if r > 0:
        neighbors.append(((r - 1, c), grid[r - 1][c]))  # N
    if r < rmax:
        neighbors.append(((r + 1, c), grid[r + 1][c]))  # S
    if c > 0:
        neighbors.append(((r, c - 1), grid[r][c - 1]))  # W
    if c < cmax:
        neighbors.append(((r, c + 1), grid[r][c + 1]))  # E

    return neighbors


def test():
    grid = load("data/day10_test.txt")
    valid_trails, trailheads = find_trails(grid)
    assert len(trailheads) == 9
    score = len(valid_trails)
    assert score == 36, score


def solve_part1():
    grid = load("data/day10_data.txt")
    valid_trails, trailheads = find_trails(grid)
    score = len(valid_trails)
    print(f"Part 1: {score}")


def solve_part2():
    grid = load("data/day10_data.txt")
    valid_trails, trailheads = find_trails(grid, distinct=True)
    score = len(valid_trails)
    print(f"Part 2: {score}")


if __name__ == "__main__":
    solve_part1()
    solve_part2()
