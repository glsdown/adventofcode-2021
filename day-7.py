import re
import sys

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [
            int(i) for i in [line.strip() for line in f.readlines()][0].split(",")
        ]

    # Complete the task
    current = max(values) * len(values)
    for i in range(min(values), max(values) + 1):
        differences = sum([abs(i - crab) for crab in values])
        if differences < current:
            current = differences

    answer = current

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [
            int(i) for i in [line.strip() for line in f.readlines()][0].split(",")
        ]

    # Complete the task
    current = max(values) * len(values) * len(values)
    for i in range(min(values), max(values) + 1):
        differences = sum([(abs(i - crab) + 1) * abs(i - crab) // 2 for crab in values])
        if differences < current:
            current = differences
    answer = current

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
