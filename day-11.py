import re
import sys

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [[int(i) for i in line.strip()] for line in f.readlines()]

    # Complete the task
    no_rows = len(values)
    no_cols = len(values[0])
    threshold = 10

    def increase_neighbours(x, y):
        if (
            x < 0
            or x >= no_cols
            or y < 0
            or y >= no_rows
            or values[y][x] > threshold
        ):
            return
        else:
            values[y][x] += 1
            if values[y][x] == threshold:
                for x_change in [-1, 0, 1]:
                    for y_change in [-1, 0, 1]:
                        if not (x_change == 0 and y_change == 0):
                            increase_neighbours(x + x_change, y + y_change)

    answer = 0
    for _ in range(100):
        for x in range(no_cols):
            for y in range(no_rows):
                increase_neighbours(x, y)
        answer += len([x for y in values for x in y if x >= threshold])
        values = [[i if i < threshold else 0 for i in line] for line in values]

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [[int(i) for i in line.strip()] for line in f.readlines()]

    # Complete the task
    no_rows = len(values)
    no_cols = len(values[0])
    threshold = 10

    def increase_neighbours(x, y):
        if (
            x < 0
            or x >= no_cols
            or y < 0
            or y >= no_rows
            or values[y][x] > threshold
        ):
            return
        else:
            values[y][x] += 1
            if values[y][x] == threshold:
                for x_change in [-1, 0, 1]:
                    for y_change in [-1, 0, 1]:
                        if not (x_change == 0 and y_change == 0):
                            increase_neighbours(x + x_change, y + y_change)

    answer = 0
    while True:
        answer += 1
        for x in range(no_cols):
            for y in range(no_rows):
                increase_neighbours(x, y)
        if (
            len([x for y in values for x in y if x >= threshold])
            == no_rows * no_cols
        ):
            break
        values = [[i if i < threshold else 0 for i in line] for line in values]

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
