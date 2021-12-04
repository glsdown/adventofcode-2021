import shutil
from pathlib import Path
import re

from aocd import get_data

HERE = Path("__file__").parent

TEMPLATE_PYTHON = """
import re
import sys

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    \"\"\"Part 1/Star 1\"\"\"

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # TODO: Complete the task
    answer = 0

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    \"\"\"Part 2/Star 2\"\"\"

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [line.strip() for line in f.readlines()]

    # TODO: Complete the task
    answer = 0

    # Print out the response
    print(f"Task 2 Answer: {answer}")


if __name__ == "__main__":
    \"\"\"
    Run using e.g.
        `python day-1.py -test`
        `python day-1.py`
        `python day-1.py -test -2`
        `python day-1.py -2`
        `python day-1.py -test -both`
        `python day-1.py -both`
    \"\"\"

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

"""


def get_next_day():
    """Identify what the next day is to load"""
    pattern = re.compile(r"day\-(\d+)")

    return (
        max(
            [
                int(pattern.match(file.stem).groups()[0])
                for file in Path(HERE).glob("day-*.py")
                if pattern.match(file.stem)
            ]
        )
        + 1
    )


def prepare_new_day():
    """Create the files for the next available day"""

    # Identify the next day to get
    next_day = get_next_day()

    # Check if the files exist already
    python_file = HERE / f"day-{next_day}.py"
    input_file = HERE / "inputs" / f"day-{next_day}.txt"
    test_input_file = HERE / "input-tests" / f"day-{next_day}.txt"
    if python_file.exists():
        raise FileExistsError(f"{input_file} already exists")
    elif test_input_file.exists():
        raise FileExistsError(f"{test_input_file} already exists")
    elif input_file.exists():
        raise FileExistsError(f"{test_input_file} already exists")

    # Get the input data
    # Run this first as if the day isn't yet available we don't want to create
    # the other files
    input_data = get_data(day=next_day, year=2021)
    with open(input_file, "w") as f:
        f.write(input_data)

    # Create an (empty) test input file
    with open(test_input_file, "w") as f:
        f.write("")

    # Create the template file
    with open(python_file, "w") as f:
        f.write(TEMPLATE_PYTHON)


if __name__ == "__main__":
    prepare_new_day()
