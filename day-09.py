import re
import sys
import numpy as np

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [
            [9] + [int(i) for i in list(line.strip())] + [9] for line in f.readlines()
        ]

    # Add boundaries to the grid
    no_cols = len(values[0])
    values = [[9] * no_cols] + values + [[9] * no_cols]
    no_rows = len(values)

    # Loop through the values
    answer = 0
    # Don't include the new 'edge' of the grid
    for x in range(1, no_cols - 1):
        for y in range(1, no_rows - 1):
            # Get the value
            value = values[y][x]

            # Identify the 'neighbours' - because we added a 'grid' around the
            # edge we don't need to worry about going 'off' the grid this way
            neighbours = [
                values[y][x + 1],
                values[y][x - 1],
                values[y + 1][x],
                values[y - 1][x],
            ]
            # Check all the neighbours are higher than it
            if all(v > value for v in neighbours):
                answer += value + 1

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [
            [9] + [int(i) for i in list(line.strip())] + [9] for line in f.readlines()
        ]

    # Add boundaries to the grid
    no_cols = len(values[0])
    values = [[9] * no_cols] + values + [[9] * no_cols]
    no_rows = len(values)

    def get_9s(new_values, x, y):
        # Base case
        if new_values[y][x] == 9 or not (0 <= x < no_cols and 0 <= y < no_rows):
            return 0
        else:
            # 'Mark' that we have seen this value
            new_values[y][x] = 9
            # Recurse the function on all the neighbours
            return (
                1
                + get_9s(new_values, x + 1, y)
                + get_9s(new_values, x - 1, y)
                + get_9s(new_values, x, y - 1)
                + get_9s(new_values, x, y + 1)
            )

    # Loop through the values
    basins = {}
    for x in range(1, no_cols - 1):
        for y in range(1, no_rows - 1):
            # Check all the neighbours (if they are in the grid)
            value = values[y][x]
            neighbours = [
                values[y][x + 1],
                values[y][x - 1],
                values[y + 1][x],
                values[y - 1][x],
            ]
            if all(v > value for v in neighbours):
                # We've found a 'low' point, now count in each direction until
                # a 9 is reached

                # Create a copy of the grid (this will be marked where we've
                # 'been' so is deliberately passed in by reference and not
                # value)
                new_values = [[i for i in line] for line in values]
                # Recurse over all the points
                basins[(x, y)] = get_9s(new_values, x, y)

    # Multiply the three largest basins
    answer = np.product(sorted([v for _, v in basins.items()])[-3:])

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
