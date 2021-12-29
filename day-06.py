import re
import sys
from collections import defaultdict

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Complete the task

    # Convert the data
    fish = [int(i) for i in values[0].split(",")]

    # Loop through the simulation
    number_days = 80
    for _ in range(number_days):
        new_fish = []
        for f in fish:
            if f == 0:
                new_fish += [6, 8]
            else:
                new_fish.append(f - 1)
        fish = [i for i in new_fish]

    answer = len(fish)

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Convert the data
    start_fish = [int(i) for i in values[0].split(",")]

    number_days = 256

    # Create a 'counts' dictionary
    fish = defaultdict(int)
    for f in start_fish:
        fish[f] += 1

    # Loop through the simulation
    for _ in range(number_days):
        spawning_fish = fish[0]

        # Decrease all fish by one
        for i in range(8):
            fish[i] = fish[i + 1]

        # Add the new fish
        fish[6] += spawning_fish  # Old fish - 6 days left
        fish[8] = spawning_fish  # New fish - 8 days left

    # Calculate the number of fish
    answer = sum(v for _, v in fish.items())

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
