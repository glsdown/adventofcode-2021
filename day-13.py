import re
import sys

import matplotlib.pyplot as plt

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Extract the input
    instructions = [i for i in values if i[:4] == "fold"]
    dots = [tuple(v.split(",")) for v in values[: -(len(instructions) + 1)]]
    dots = set([(int(x), int(y)) for x, y in dots])

    # look at the first fold only
    fold = instructions[0].split()[-1]
    line = int(fold.split("=")[-1])
    new_dots = set()
    # check if the fold is x or y
    if fold[0] == "y":
        for d in dots:
            if d[1] > line:
                new_dots.add((d[0], line - (d[1] - line)))
            else:
                new_dots.add(d)
    elif fold[0] == "x":
        for d in dots:
            if d[0] > line:
                new_dots.add((line - (d[0] - line), d[1]))
            else:
                new_dots.add(d)

    answer = len(new_dots)

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Extract the input
    instructions = [i for i in values if i[:4] == "fold"]
    dots = [tuple(v.split(",")) for v in values[: -(len(instructions) + 1)]]
    dots = set([(int(x), int(y)) for x, y in dots])

    # look at the first fold only
    for instruction in instructions:
        fold = instruction.split()[-1]
        line = int(fold.split("=")[-1])
        new_dots = set()
        # check if the fold is x or y
        if fold[0] == "y":
            for d in dots:
                if d[1] > line:
                    new_dots.add((d[0], line - (d[1] - line)))
                else:
                    new_dots.add(d)
        elif fold[0] == "x":
            for d in dots:
                if d[0] > line:
                    new_dots.add((line - (d[0] - line), d[1]))
                else:
                    new_dots.add(d)

        dots = new_dots

    graph_dots = list(dots)
    x = [i[0] for i in graph_dots]
    y = [-i[1] for i in graph_dots]

    # plot our list in X,Y coordinates
    plt.scatter(x, y)
    plt.show()

    # Print out the response
    # print(f"Task 2 Answer: {answer}")


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
