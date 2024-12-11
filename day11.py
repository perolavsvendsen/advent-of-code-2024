"""Advent of Code - Day 11"""

from pathlib import Path


class Stone:
    def __init__(self, initial_marking: int):
        self.marking = initial_marking

    def __repr__(self):
        return str(self.marking)

    def change(self):
        """Change the marking according to the rules."""
        if self.marking == 0:
            self.marking = 1
        elif len(str(self.marking)) % 2 == 0:
            s = str(self.marking)
            first_half = int(s[: len(s) // 2])
            second_half = int(s[len(s) // 2 :])
            self.marking = first_half  # keep this Stone
            return second_half  # for spawning new Stone
        else:
            self.marking = self.marking * 2024


def blink(markings, iters):

    stones = [Stone(marking) for marking in markings]

    for i in range(iters):
        current_stones = [stone for stone in stones]
        for s, stone in enumerate(current_stones):
            change_result = stone.change()  # change the stones
            if change_result is not None:
                stones.append(Stone(change_result))  # spawn new stone

                # ignoring instruction that order shall be preserved...

    return stones


def test_blink():
    stones = load("data/day11_test.txt")

    assert len(blink(stones, 2)) == 4
    assert len(blink(stones, 6)) == 22
    assert len(blink(stones, 25)) == 55312


def load(fname):
    return [int(n) for n in Path(fname).read_text(encoding="utf-8").split()]


def solve_part1():
    stones = load("data/day11_data.txt")
    print(f"Part 1: {len(blink(stones, 25))}")


def solve_part2():
    stones = load("data/day11_data.txt")
    print(f"Part 2: {len(blink(stones, 75))}")


if __name__ == "__main__":
    solve_part1()
    # solve_part2()
