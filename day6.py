"""Advent of Code - Day 6"""


def load(fname):
    with open(fname, "r", encoding="utf-8") as f:
        return [list(line.strip()) for line in f.readlines()]


def find_guard(map_):
    for r, row in enumerate(map_):
        if "^" in row:
            return r, row.index("^")

    raise ValueError("Guard not found.")


def test_play():
    map_ = load("data/day6_test.txt")
    assert play(map_) == 41


def test_find_possible_loops():
    map_ = load("data/day6_test.txt")
    assert find_possible_loops(map_) == 6


def find_possible_loops(map_):
    loops_found = 0
    for r, row in enumerate(map_):
        for c, col in enumerate(row):

            # already obstacle?
            if map_[r][c] == "#":
                continue

            # guard is here?
            elif map_[r][c] == "^":
                continue

            # place obstacle and run the modified map to check for loop
            elif map_[r][c] == ".":
                modified_map = copy(map_)
                modified_map[r][c] = "#"
                if play(modified_map) == -1:
                    # print("Found loop")
                    loops_found += 1

            else:

                raise ValueError("wtf")

    return loops_found


def copy(input: list):
    output = []
    for row in input:
        output.append([c for c in row])

    return output


def play(map_):

    maxrow = len(map_) - 1
    maxcol = len(map_[0]) - 1
    row, col = find_guard(map_)

    point = "N"

    i = 0

    while 0 <= row <= maxrow and 0 <= col <= maxcol:

        i += 1

        # get next step
        nextrow, nextcol = next_step(row, col, point)

        # next step will be outside edge of map?
        if nextrow < 0 or nextrow > maxrow or nextcol < 0 or nextcol > maxcol:
            map_[row][col] = "X"
            break

        # next step will hit obstacle?
        elif map_[nextrow][nextcol] == "#":
            point = turn_90(point)
            continue

        else:
            # move to next position
            map_[row][col] = "X"
            row = nextrow
            col = nextcol

        if i > 10000:
            # assume loop
            return -1

    return sum([line.count("X") for line in map_])


def next_step(row, col, point):
    if point == "N":
        return row - 1, col
    elif point == "S":
        return row + 1, col
    elif point == "E":
        return row, col + 1
    elif point == "W":
        return row, col - 1

    raise ValueError


def turn_90(point):
    turns = {"N": "E", "E": "S", "S": "W", "W": "N"}
    return turns[point]


def solve_part1():
    map_ = load("data/day6_data.txt")
    result = play(map_)
    print(f"Part 1: {result}")


def solve_part2():
    map_ = load("data/day6_data.txt")
    result = find_possible_loops(map_)
    assert result < 14672, result
    print(f"Part 2: {result}")


if __name__ == "__main__":
    solve_part1()
    solve_part2()
