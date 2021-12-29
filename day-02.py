import re
import sys

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Complete the task
    instructions = [[j[0], int(j[1])] for j in [i.split() for i in values]]
    horizontal = sum([i[1] for i in instructions if i[0] == "forward"])
    depth = sum([i[1] for i in instructions if i[0] == "down"]) - sum(
        [i[1] for i in instructions if i[0] == "up"]
    )

    answer = horizontal * depth

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Complete the task
    instructions = [[j[0], int(j[1])] for j in [i.split() for i in values]]
    aim = 0
    horizontal = 0
    depth = 0

    for command, value in instructions:
        if command == "down":
            aim += value
        elif command == "up":
            aim -= value
        else:
            horizontal += value
            depth += aim * value

    answer = horizontal * depth

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
