import re
import sys

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    values = [i.split(" | ") for i in values]

    # Complete the task
    options = {
        0: "abcefg",
        1: "cf",
        2: "acdeg",
        3: "acdfg",
        4: "bcdf",
        5: "abdfg",
        6: "abdefg",
        7: "acf",
        8: "abcdefg",
        9: "abcdfg",
    }
    # Want to find 1, 4, 7 or 8
    to_find = [1, 4, 7, 8]
    to_find_lengths = [len(options[i]) for i in to_find]

    answer = 0
    for _, value in values:
        answer += sum([len(i) in to_find_lengths for i in value.split()])

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    values = [i.split(" | ") for i in values]

    # Length 2 is 1 = cf
    # Length 4 is 4 = bcdf
    # Length 3 is 7 = acf
    # Length 7 is 8 = abcdefg
    # Length 6 is either 0, 6 or 9
    # Length 5 is either 2, 3, 5

    def order_alpha(x):
        return "".join(sorted(x))

    answer = 0
    for digits, value in values:
        all_digits = [order_alpha(i) for i in digits.split()]
        key_table = {}
        # Unique lengths
        key_table[1] = [i for i in all_digits if len(i) == 2][0]
        key_table[4] = [i for i in all_digits if len(i) == 4][0]
        key_table[7] = [i for i in all_digits if len(i) == 3][0]
        key_table[8] = [i for i in all_digits if len(i) == 7][0]
        # 6 character ones
        key_table[6] = [
            i
            for i in all_digits
            if len(i) == 6 and not all(j in i for j in key_table[1])
        ][
            0
        ]  # both 9 and 0 have the same digits as in 1
        key_table[9] = [
            i
            for i in all_digits
            if len(i) == 6 and all(j in i for j in key_table[4]) and i != key_table[6]
        ][
            0
        ]  # both 6 and 9 jave the same digits as 4
        key_table[0] = [
            i
            for i in all_digits
            if len(i) == 6 and i != key_table[6] and i != key_table[9]
        ][
            0
        ]  # 0 isn't 6 or 9
        # 5 character ones
        key_table[2] = [
            i
            for i in all_digits
            if len(i) == 5 and not all(j in key_table[9] for j in i)
        ][
            0
        ]  # both 5 and 3 have all their digits in 9
        key_table[5] = [
            i for i in all_digits if len(i) == 5 and all(j in key_table[6] for j in i)
        ][
            0
        ]  # 5 has all its digits in 6
        key_table[3] = [
            i
            for i in all_digits
            if len(i) == 5 and i != key_table[5] and i != key_table[2]
        ][
            0
        ]  # 3 isn't 5 or 2
        code_lookup = {v: str(k) for k, v in key_table.items()}
        answer += int("".join([code_lookup[order_alpha(v)] for v in value.split()]))

    # Print out the response
    print(f"Task 2 Answer: {answer}")


if __name__ == "__main__":
    """
    Run using e.g.
        `python day-1.py -test`
        `python day-1.py`
        `python day-1.py -test -2`
        `python day-1.py -2`
        `python day-1.py -test -both`
        `python day-1.py -both`
    """

    # Identify the folder that the input is in
    test = "-test" in sys.argv
    if test:
        path = "input-tests"
    else:
        path = "inputs"

    # Identify which one to run - 1 is default
    if "-2" in sys.argv:
        part_2(path)
    elif "-both" in sys.argv:
        part_1(path)
        part_2(path)
    else:
        part_1(path)
