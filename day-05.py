import re
import sys
from collections import defaultdict

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [
            [[int(k) for k in j.split(",")] for j in line.strip().split(" -> ")]
            for line in f.readlines()
        ]

    # Complete the task

    # Identify the valid lines
    values = [i for i in values if (i[0][0] == i[1][0]) ^ (i[0][1] == i[1][1])]

    seen_dict = defaultdict(int)

    for vent1, vent2 in values:
        # Check if the first value is the one fixed
        if vent1[0] == vent2[0]:
            if vent2[1] >= vent1[1]:
                step = 1
            else:
                step = -1
            # Create all the coordinates
            for i in range(vent1[1], vent2[1] + step, step):
                new_value = (vent1[0], i)
                # If the coordinate has already been on a line, add to the
                # counter
                seen_dict[new_value] += 1
        elif vent1[1] == vent2[1]:
            # Do the same but for the second one
            if vent2[0] >= vent1[0]:
                step = 1
            else:
                step = -1
            for i in range(vent1[0], vent2[0] + step, step):
                new_value = (i, vent1[1])
                seen_dict[new_value] += 1

    answer = len([i for _, i in seen_dict.items() if i > 1])

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [
            [[int(k) for k in j.split(",")] for j in line.strip().split(" -> ")]
            for line in f.readlines()
        ]

    seen_dict = defaultdict(int)

    for vent1, vent2 in values:

        # Check if the first value is the one fixed
        if vent1[0] == vent2[0]:
            if vent2[1] >= vent1[1]:
                step = 1
            else:
                step = -1
            # Create all the coordinates
            for i in range(vent1[1], vent2[1] + step, step):
                new_value = (vent1[0], i)
                # If the coordinate has already been on a line, add to the
                # counter
                seen_dict[new_value] += 1
        elif vent1[1] == vent2[1]:
            # Do the same but for the second one
            if vent2[0] >= vent1[0]:
                step = 1
            else:
                step = -1
            for i in range(vent1[0], vent2[0] + step, step):
                new_value = (i, vent1[1])
                seen_dict[new_value] += 1
        else:
            # Deal with diagonals

            # Identify the steps
            step = [1, 1]
            for i in [0, 1]:
                if vent2[i] < vent1[i]:
                    step[i] = -1

            # Zip the diagonals together
            diags = list(
                zip(
                    range(vent1[0], vent2[0] + step[0], step[0]),
                    range(vent1[1], vent2[1] + step[1], step[1]),
                )
            )

            # Check which coordinates have been seen
            for new_value in diags:
                seen_dict[new_value] += 1

    answer = len([i for _, i in seen_dict.items() if i > 1])

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
