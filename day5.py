"""Advent of Code - Day 5"""

from pathlib import Path


def load(fname):
    """Load text from file."""
    data = Path(fname, encoding="utf-8").read_text()

    rules = []
    updates = []

    read_sorting = True
    for line in data.split("\n"):
        if line == "":
            read_sorting = False
            continue
        if read_sorting:
            rules.append(line)
        else:
            updates.append([int(u) for u in line.split(",")])

    return rules, updates


def is_valid(rules, update):
    """Check that the update is correctly sorted."""

    rules = dictify_rules(rules)

    for e, elem in enumerate(update):
        if elem not in rules:
            # not rule
            continue
        afters = rules[elem]
        for after in afters:
            if after in update[0:e]:
                return False
    return True


def find_valid_updates(rules, updates):
    """Return valid updates."""
    return [upd for upd in updates if is_valid(rules, upd)]


def sum_middle_values(rules, updates):
    """Return sum of middle values."""
    return sum([find_middle(update) for update in updates])


def dictify_rules(rules_raw):
    rules = {}
    for rule in rules_raw:
        before, after = int(rule.split("|")[0]), int(rule.split("|")[1])
        if before in rules:
            rules[before].append(after)
        else:
            rules[before] = [after]

    return rules


def find_invalid_updates(rules, updates):
    """Find and return the incorrect updates only."""
    return [update for update in updates if is_valid(rules, update) is False]


def test_find_invalid_updates():
    rules, updates = load("data/day5_test.txt")
    assert [61, 13, 29] in find_invalid_updates(rules, updates)
    assert [75, 97, 47, 61, 53] in find_invalid_updates(rules, updates)
    assert [97, 13, 75, 29, 47] in find_invalid_updates(rules, updates)


def find_middle(array):
    return array[len(array) // 2]


def correctify_update(rules, incorrect_update):
    """Provided update is incorrect. Make them correct according to the rules."""
    rules = dictify_rules(rules)

    update = [u for u in incorrect_update]

    for i in range(10):  # iterate
        for e, elem in enumerate(incorrect_update):
            if elem in rules:
                afters = rules[elem]
            else:
                continue

            for after in afters:
                if after in update[0:e]:
                    # an after is before the elem, so move elem to before the after.
                    update.remove(elem)
                    update.insert(update.index(after), elem)

        incorrect_update = [u for u in update]

    return update


def test_correctify_update():
    """Given an incorrect update, make it correct."""
    rules, _ = load("data/day5_test.txt")
    assert correctify_update(rules, [61, 13, 29]) == [61, 29, 13]
    assert correctify_update(rules, [75, 97, 47, 61, 53]) == [97, 75, 47, 61, 53]
    assert correctify_update(rules, [97, 13, 75, 29, 47]) == [97, 75, 47, 29, 13]


def test_is_valid():
    rules, _ = load("data/day5_test.txt")
    assert is_valid(rules, [75, 97, 47, 61, 53]) is False
    assert is_valid(rules, [75, 47, 61, 53, 29])


def test_find_middle():
    assert find_middle([75, 97, 47, 61, 53]) == 47


def test():
    rules, updates = load("data/day5_test.txt")
    valid_updates = find_valid_updates(rules, updates)
    assert sum_middle_values(rules, valid_updates) == 143

    invalid_updates = find_invalid_updates(rules, updates)
    corrected_updates = [correctify_update(rules, upd) for upd in invalid_updates]
    assert sum_middle_values(rules, corrected_updates) == 123


def solve_part1():
    rules, updates = load("data/day5_data.txt")
    valid_updates = [upd for upd in updates if is_valid(rules, upd)]
    result = sum_middle_values(rules, valid_updates)
    print(f"Part 1: {result}")


def solve_part2():
    rules, updates = load("data/day5_data.txt")
    incorrect_updates = find_invalid_updates(rules, updates)
    corrected_updates = [correctify_update(rules, upd) for upd in incorrect_updates]

    for update in corrected_updates:
        if not is_valid(rules, update):
            raise ValueError(f"Not valid: {update}")

    result = sum([find_middle(update) for update in corrected_updates])
    print(f"Part 2: {result}")


if __name__ == "__main__":
    solve_part1()
    solve_part2()
