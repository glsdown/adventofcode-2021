import re
import sys
from cachetools import cached
from collections import defaultdict, Counter

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Get the data
    template = values[0]
    rules = [r.split(" -> ") for r in values[2:]]

    # Create the rule replacements
    rules = defaultdict(str, {r[0]: r[1] for r in rules})

    for _ in range(10):
        # Loop through each pair
        polymer = ""
        for index in range(1, len(template)):
            current_pair = template[index - 1 : index + 1]
            polymer += template[index - 1] + rules[current_pair]

        # Add the last letter
        polymer += template[-1]

        # Reassign as the start point
        template = polymer

    # Get the letter counts
    counts = Counter(polymer)

    # Calculate the requested answer
    answer = max(counts.values()) - min(counts.values())

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def add_dictionaries(*args):

    result = defaultdict(int)
    for arg in args:
        for key, item in arg.items():
            result[key] += item

    return result


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Get the data
    template = values[0]
    rules = [r.split(" -> ") for r in values[2:]]

    # Create the rule replacements
    rules = defaultdict(str, {r[0]: r[1] for r in rules})

    # Create recursive function
    @cached(cache={})
    def get_counts(pair, n):
        if n == 0:
            return {}
        else:
            return add_dictionaries(
                get_counts(f"{pair[0]}{rules[pair]}", n - 1),
                get_counts(f"{rules[pair]}{pair[1]}", n - 1),
                {rules[pair]: 1},
            )

    # Run for x turns
    turns = 40
    start = Counter(template)
    results = [
        get_counts(template[i - 1 : i + 1], turns)
        for i in range(1, len(template))
    ]
    counts = add_dictionaries(start, *results)

    # Get the answer
    answer = max(counts.values()) - min(counts.values())

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
