"""Advent of Code - Day 9"""

from pathlib import Path
import time
import itertools


class File:
    def __init__(self, id, size):
        self.id = int(id)
        self.size = int(size)
        self.file = True
        self.free = False

    def __repr__(self):
        return str(self.id) * self.size


class Free:
    def __init__(self, size):
        self.size = int(size)
        self.free = True
        self.file = False

    def __repr__(self):
        return "." * self.size


def load(fname):
    diskmap = Path(fname).read_text()

    blocks = []
    id_ = 0
    for i, size in enumerate(diskmap):
        if i % 2 == 0:
            for block in range(int(size)):
                blocks.append(id_)
            id_ += 1
        else:
            for block in range(int(size)):
                blocks.append(".")
    return blocks


def load_whole_files(fname):
    diskmap = Path(fname).read_text()

    blocks = []
    id_ = 0
    for i, size in enumerate(diskmap):
        if int(size):
            if i % 2 == 0:
                blocks.append(File(id_, size))
                id_ += 1
            else:
                blocks.append(Free(size))

    return blocks


def test_defragment():
    blocks = load("data/day9_test.txt")
    defragmented = defragment(blocks)
    result = make_checksum(defragmented)
    assert result == 1928, result


def defragment(blocks):

    t0 = time.time()

    checksum = 0

    while True:
        last_number_index = find_last_number(blocks)
        first_free_index = blocks.index(".")

        if first_free_index > last_number_index:
            return blocks

        blocks[first_free_index], blocks[last_number_index] = (
            blocks[last_number_index],
            blocks[first_free_index],
        )


def defragment_whole_files(blocks):

    files = reversed([item for item in blocks if item.file])

    counter = 0

    for file in files:
        if counter in [100, 500, 1000, 2000]:
            print(f"{counter} / {len(files)}")
        file_index = blocks.index(file)  # find_last_file_index(blocks, ignores)

        # where can we place it?
        try:
            free_index = find_first_free_larger_than(blocks, file.size)
        except IndexError:
            # could not find a spot, continue to next.
            # ignores.append(file)
            continue

        if free_index > file_index:
            # not moving files towards the right, continue
            continue

        free = blocks[free_index]  # use this free space to place the file

        blocks.pop(file_index)  # pop file from blocks
        blocks.insert(file_index, Free(file.size))  # insert free blocks
        blocks.insert(free_index, file)  # insert it before the free
        free.size -= file.size  # reduce size of free space accordingly

    final_array = blocks_to_str(blocks)

    return final_array


def test_defragment_whole_files():
    blocks = load_whole_files("data/day9_test.txt")
    defragmented = defragment_whole_files(blocks)
    print(make_checksum(blocks_to_str(blocks)))


def blocks_to_str(blocks):
    final_array = []
    for item in blocks:
        if item.file:
            final_array += [item.id for _ in range(item.size)]
        elif item.free:
            final_array += ["." for _ in range(item.size)]
        else:
            raise ValueError("wtf")

    return final_array


def find_first_free_larger_than(blocks, size):
    for i, item in enumerate(blocks):
        if item.free and item.size >= size:
            return i
    raise IndexError("Could not find first free.")


def find_last_file_index(blocks, ignores):
    for ri, item in enumerate(reversed(blocks)):
        if item.file and item not in ignores:
            return len(blocks) - ri - 1
    raise IndexError("Could not find last file.")


def find_last_number(blocks):
    for ri, item in enumerate(reversed(blocks)):
        if item != ".":
            return len(blocks) - ri - 1
    return -1


def make_checksum(blocks):
    return sum([i * item for i, item in enumerate(blocks) if item != "."])


def make_checksum_whole_files(blocks):
    return sum([i * item.size for i, item in enumerate(blocks) if item.file])


def solve_part1():
    blocks = load("data/day9_data.txt")
    defragmented = defragment(blocks)
    result = make_checksum(defragmented)
    print(f"Part 1: {result}")


def solve_part2():
    blocks = load_whole_files("data/day9_data.txt")
    defragmented = defragment_whole_files(blocks)
    result = make_checksum(blocks_to_str(blocks))  # <-- HAHA WTF!
    print(f"Part 2: {result}")


if __name__ == "__main__":
    solve_part1()
    solve_part2()
