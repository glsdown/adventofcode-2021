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
    illegal = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    opposites = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<",
    }
    answer = 0
    for line in values:
        current = []
        for value in line:
            if value in "[({<":
                current.append(value)
            else:
                if opposites[value] != current[-1]:
                    answer += illegal[value]
                    break
                else:
                    current = current[:-1]

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # Complete the task
    points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    opposites = {
        ")": "(",
        "]": "[",
        "}": "{",
        ">": "<",
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">",
    }
    answer = []
    for line in values:
        current = []
        illegal = False
        for value in line:
            if value in "[({<":
                current.append(value)
            else:
                if opposites[value] != current[-1]:
                    illegal = True
                    break
                else:
                    current = current[:-1]

        if not illegal:
            if len(current) > 0:
                score = 0
                completion = "".join([opposites[i] for i in current[::-1]])
                for char in completion:
                    score *= 5
                    score += points[char]
                answer.append(score)

    answer = sorted(answer)[len(answer) // 2]

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
