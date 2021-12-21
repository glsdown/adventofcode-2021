import re
import sys

# Get the day from the filename e.g. day-1.py
DAY = re.match(r"day\-(\d+)\.py", sys.argv[0]).groups()[0]


def part_1(path):
    """Part 1/Star 1"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        targets = [line.strip() for line in f.readlines()][0]

    # Get the values
    targets = [
        i.split("..")
        for i in list(
            re.match(
                r"target area\: x\=(\-?\d+\.\.\-?\d+)\, y\=(\-?\d+\.\.\-?\d+)",
                targets,
            ).groups()
        )
    ]

    # Convert to x, y ranges
    targets = {
        "x": [int(targets[0][0]), int(targets[0][1])],
        "y": [int(targets[1][0]), int(targets[1][1])],
    }

    # These are based on the assumption that the target is 'positive' x and
    # 'negative' y.

    # Want to get the 'highest' y, so should always shoot 'up'
    lower_limit_y = 0
    # First 'jump' down below the starting point is always the first jump
    # 'up' plus one
    upper_limit_y = abs(targets["y"][0]) + 1

    # Need to move to the right
    lower_limit_x = 0
    # Can't 'overshoot'
    upper_limit_x = targets["x"][1] + 1

    # Create variable to keep track
    answer = 0

    for x in range(lower_limit_x, upper_limit_x + 1):
        for y in range(lower_limit_y, upper_limit_y + 1):

            # Get the start position
            position = [0, 0]

            # Create the initial velocity
            velocity = [x, y]

            # Current max
            current_max = 0

            # Loop through each turn
            while True:

                # Increase by the velocity
                position[0] += velocity[0]
                position[1] += velocity[1]

                # Update the max y position
                current_max = max([position[1], current_max])

                # Change the velocity due to drag
                if velocity[0] < 0:
                    velocity[0] += 1
                elif velocity[0] > 0:
                    velocity[0] -= 1
                velocity[1] -= 1

                # Check for win
                if (
                    targets["x"][0] <= position[0] <= targets["x"][1]
                    and targets["y"][0] <= position[1] <= targets["y"][1]
                ):
                    answer = max([answer, current_max])
                    break

                # Check for loss
                # As above assumes positive x range, and negative y range
                if (
                    position[0] > targets["x"][1]
                    or position[1] < targets["y"][0]
                ):
                    break

    # Print out the response
    print(f"Task 1 Answer: {answer}")


def part_2(path):
    """Part 2/Star 2"""

    # Open the file
    with open(f"{path}/day-{DAY}.txt", "r") as f:
        targets = [line.strip() for line in f.readlines()][0]

    # Get the values
    targets = [
        i.split("..")
        for i in list(
            re.match(
                r"target area\: x\=(\-?\d+\.\.\-?\d+)\, y\=(\-?\d+\.\.\-?\d+)",
                targets,
            ).groups()
        )
    ]

    # Convert to x, y ranges
    targets = {
        "x": [int(targets[0][0]), int(targets[0][1])],
        "y": [int(targets[1][0]), int(targets[1][1])],
    }

    # These are based on the assumption that the target is 'positive' x and
    # 'negative' y.

    # Can't shoot below the bottom of the box
    lower_limit_y = targets["y"][0] - 1
    # First 'jump' down below the starting point is always the first jump
    # 'up' plus one
    upper_limit_y = abs(targets["y"][0]) + 1

    # Need to move to the right (starts negative - never gets positive)
    lower_limit_x = 0
    # Can't 'overshoot'
    upper_limit_x = targets["x"][1] + 1

    # Create variable to keep track of successful ones
    answer = set()

    for x in range(lower_limit_x, upper_limit_x + 1):
        for y in range(lower_limit_y, upper_limit_y + 1):

            # Get the start position
            position = [0, 0]

            # Create the initial velocity
            velocity = [x, y]

            # Loop through each turn
            while True:

                # Increase by the velocity
                position[0] += velocity[0]
                position[1] += velocity[1]

                # Change the velocity due to drag
                if velocity[0] < 0:
                    velocity[0] += 1
                elif velocity[0] > 0:
                    velocity[0] -= 1
                velocity[1] -= 1

                # Check for win
                if (
                    targets["x"][0] <= position[0] <= targets["x"][1]
                    and targets["y"][0] <= position[1] <= targets["y"][1]
                ):
                    answer.add((x, y))
                    break

                # Check for loss
                # As above assumes positive x range, and negative y range
                if (
                    position[0] > targets["x"][1]
                    or position[1] < targets["y"][0]
                ):
                    break

    # Print out the response
    print(f"Task 2 Answer: {len(answer)}")


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
