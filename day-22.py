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

    pattern = re.compile(
        r"(on|off) x\=(\-?\d+)\.\.(\-?\d+)\,y\=(\-?\d+)\.\.(\-?\d+)\,z"
        r"\=(\-?\d+)\.\.(\-?\d+)"
    )

    # Create the grid
    options = defaultdict(int)

    # Keep track of the number 'on'
    answer = 0

    # Loop through each instruction
    for counter, line in enumerate(values):
        instructions = pattern.match(line).groups()

        # Get the correct bits and remove the 'unwanted' parts
        on = int(instructions[0] == "on")
        value_range = [
            [
                i
                for i in range(
                    max([-50, int(instructions[1])]),
                    min([50, int(instructions[2])]) + 1,
                )
            ],
            [
                i
                for i in range(
                    max([-50, int(instructions[3])]),
                    min([50, int(instructions[4])]) + 1,
                )
            ],
            [
                i
                for i in range(
                    max([-50, int(instructions[5])]),
                    min([50, int(instructions[6])]) + 1,
                )
            ],
        ]

        # Create all the co-ordinates
        for x in value_range[0]:
            for y in value_range[1]:
                for z in value_range[2]:
                    if (
                        x in range(-50, 51)
                        and y in range(-50, 51)
                        and z in range(-50, 51)
                    ):
                        # Count that a new one is on...
                        if on and not options[(x, y, z)]:
                            answer += 1
                        # Remove the counter if it's switching off
                        elif (not on) and options[(x, y, z)]:
                            answer -= 1
                        # Mark what the co-ordinate is
                        options[(x, y, z)] = on

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def intersect_cubes(cube_1, cube_2):
    """Get the intersections of two cubes"""

    x = (
        max([cube_1[0][0], cube_2[0][0]]),
        min([cube_1[0][1], cube_2[0][1]]),
    )

    y = (
        max([cube_1[1][0], cube_2[1][0]]),
        min([cube_1[1][1], cube_2[1][1]]),
    )

    z = (
        max([cube_1[2][0], cube_2[2][0]]),
        min([cube_1[2][1], cube_2[2][1]]),
    )

    return (x, y, z)


def part_2(path):
    """Part 2/Star 2"""

    # Pattern for each line
    pattern = re.compile(
        r"(on|off) x\=(\-?\d+)\.\.(\-?\d+)\,y\=(\-?\d+)\.\.(\-?\d+)\,z"
        r"\=(\-?\d+)\.\.(\-?\d+)"
    )

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        values = [
            pattern.match(line.strip()).groups() for line in f.readlines()
        ]

    # Split each into the correct parts
    values = [
        {
            "on": v[0] == "on",
            "x": (int(v[1]), int(v[2])),
            "y": (int(v[3]), int(v[4])),
            "z": (int(v[5]), int(v[6])),
        }
        for v in values
    ]

    # Keep track of the number 'on'
    possible_cubes = defaultdict(int)

    def cube_size(cube):

        # Get the dimensions
        x = max(0, cube[0][1] - cube[0][0] + 1)
        y = max(0, cube[1][1] - cube[1][0] + 1)
        z = max(0, cube[2][1] - cube[2][0] + 1)

        # Calculate the total size
        return x * y * z

    # Loop through each instruction
    for instruction in values:

        # Get whether it is on or off
        on = instruction["on"]

        # Get the x, y and z ranges
        x = instruction["x"]  # (min, max)
        y = instruction["y"]  # (min, max)
        z = instruction["z"]  # (min, max)

        # Create the co-ordinates for this cube
        this_cube = (x, y, z)

        # Check the intersection of this cube with every other one
        for other, weight in list(possible_cubes.items()):
            inter = intersect_cubes(other, this_cube)
            if cube_size(inter) > 0:
                possible_cubes[inter] -= weight

        # Add the 'on' co-ordinate
        if on:
            possible_cubes[this_cube] += 1

    # Find the number 'on'
    answer = 0
    for cube, weight in possible_cubes.items():
        # Size of each cube, multiply by weight and sum

        # Add to the running total
        answer += cube_size(cube) * weight

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
